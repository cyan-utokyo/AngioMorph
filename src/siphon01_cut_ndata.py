import os
import vtk
import torch
import torch.nn as nn
import numpy as np
from vtk.util import numpy_support
from scipy.interpolate import interp1d

# ==========================================
# 1. 全局配置 (Configuration)
# ==========================================
class Config:
    # --- 路径设置 ---
    NEW_DATA_DIR = r"D:\!_Nagahama_src\20250523_all\20250523_all\002_ICA_vmtk_centerline_geometry"
    OUTPUT_DIR = os.path.join(NEW_DATA_DIR, "labeled_siphon_vtk")
    MODEL_PATH = "siphon_locator_best.pth" # 确保这是你训练好的模型路径

    # --- 关键：方向控制 ---
    # 训练时你用了 REVERSE_COORDS = True，这里保留记录（仅用于理解）
    # ⚠️ 推理时的反转设置：
    # 如果新数据的方向和未反转的原始数据相反，这里设为 True；否则设为 False。
    # 你可以先设为 True 试运行，看结果对不对。
    REVERSE_NEW_DATA = True  

    # --- 其他参数 ---
    INPUT_RESAMPLE_NUM = 120
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==========================================
# 2. 基础工具 (Utils)
# ==========================================
def resample_array(arr, target_len):
    if len(arr) == target_len: return arr
    x_old = np.linspace(0, 1, len(arr))
    x_new = np.linspace(0, 1, target_len)
    f = interp1d(x_old, arr, kind='linear', axis=0, fill_value="extrapolate")
    return f(x_new)

# ==========================================
# 3. 模型定义 (需与训练时一致)
# ==========================================
class SiphonLocator(nn.Module):
    def __init__(self):
        super(SiphonLocator, self).__init__()
        self.features = nn.Sequential(
            nn.Conv1d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool1d(2)
        )
        self.regressor = nn.Sequential(
            nn.Flatten(), nn.Linear(1920, 64), nn.ReLU(),
            nn.Linear(64, 2), nn.Sigmoid()
        )
    def forward(self, x):
        feat = self.features(x)
        return self.regressor(feat)

# ==========================================
# 4. 推理类 (Predictor)
# ==========================================
class SiphonPredictor:
    def __init__(self, model_path):
        self.device = Config.DEVICE
        self.model = SiphonLocator().to(self.device)
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"✅ Loaded model from {model_path}")
        else:
            print(f"❌ Model not found at {model_path}")
        self.model.eval()
    
    def predict(self, original_coords):
        # 1. 这里的 original_coords 已经是根据配置反转/未反转过的
        
        # 2. 重采样 & 归一化 (必须与训练时一致)
        resampled = resample_array(original_coords, Config.INPUT_RESAMPLE_NUM)
        centroid = np.mean(resampled, axis=0)
        norm_input = resampled - centroid
        
        # 3. 推理
        tensor = torch.from_numpy(norm_input).float().permute(1, 0).unsqueeze(0).to(self.device)
        with torch.no_grad():
            pred = self.model(tensor).cpu().numpy()[0]
            
        return pred[0], pred[1] # t_start, t_end

# ==========================================
# 5. 文件处理与主逻辑 (已修复反转逻辑)
# ==========================================

def extract_raw_coords(filepath, reverse=False):
    """
    提取坐标，并根据 reverse 参数决定是否反转顺序
    """
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(filepath)
    reader.Update()
    polydata = reader.GetOutput()
    
    if polydata.GetNumberOfLines() < 1: return None

    line = polydata.GetLines().GetData()
    line_np = numpy_support.vtk_to_numpy(line)
    line_point_ids = line_np[1:] 
    
    # 提取点坐标
    coords = np.array([polydata.GetPoint(pid) for pid in line_point_ids])
    
    # === 关键修正：这里应用反转 ===
    if reverse:
        coords = np.flip(coords, axis=0)
        
    return coords

def save_labeled_vtk(input_path, output_path, t_start, t_end, reverse_applied):
    """
    保存 VTK，注意：
    如果读取时反转了坐标，模型的输出 t_start/t_end 是基于反转后序列的。
    写入原文件时，需要把比例映射回原始方向，或者把 Label 数组反转后再写入。
    这里采用：直接计算对应的 PointID，处理反转逻辑。
    """
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(input_path)
    reader.Update()
    polydata = reader.GetOutput()
    
    lines = polydata.GetLines()
    if lines.GetNumberOfCells() == 0: return False
    
    lines.InitTraversal()
    id_list = vtk.vtkIdList()
    lines.GetNextCell(id_list)
    n_points = id_list.GetNumberOfIds()
    
    # === 关键逻辑：坐标反转后的索引映射 ===
    # 模型输出的是在 "当前处理序列" 中的比例
    # 如果 reverse_applied=True，说明当前序列是原始序列的倒序
    # 那么 0.1 (前端) 实际上对应原始序列的 0.9 (后端)
    
    if reverse_applied:
        # 如果反转了，真实的 start/end 在原始序列中的比例应该是 (1 - t)
        # 且要注意 start/end 的交换
        real_t_start = 1.0 - t_end
        real_t_end = 1.0 - t_start
    else:
        real_t_start = t_start
        real_t_end = t_end
        
    # 计算原始 PointID 索引
    idx_s = int(real_t_start * (n_points - 1))
    idx_e = int(real_t_end * (n_points - 1))
    
    # 排序保护
    if idx_s > idx_e: idx_s, idx_e = idx_e, idx_s
    idx_s = max(0, idx_s)
    idx_e = min(idx_e, n_points - 1)
    
    # 标记
    labels = np.zeros(polydata.GetNumberOfPoints(), dtype=np.int32)
    for i in range(idx_s, idx_e + 1):
        pid = id_list.GetId(i)
        labels[pid] = 1
        
    vtk_arr = numpy_support.numpy_to_vtk(labels, deep=True, array_type=vtk.VTK_INT)
    vtk_arr.SetName("SiphonLabel")
    polydata.GetPointData().AddArray(vtk_arr)
    
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(output_path)
    writer.SetInputData(polydata)
    writer.Write()
    return True

def batch_inference():
    if not os.path.exists(Config.NEW_DATA_DIR):
        print("❌ New data directory not found.")
        return
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)
        
    predictor = SiphonPredictor(Config.MODEL_PATH)
    files = [f for f in os.listdir(Config.NEW_DATA_DIR) if f.endswith(".vtk")]
    
    print(f"\n🚀 Processing {len(files)} files with REVERSE_NEW_DATA = {Config.REVERSE_NEW_DATA}...")
    
    count = 0
    for fname in files:
        in_path = os.path.join(Config.NEW_DATA_DIR, fname)
        out_path = os.path.join(Config.OUTPUT_DIR, fname.replace(".vtk", "_labeled.vtk"))
        
        # 1. 读取坐标（应用 Config 中的反转设置）
        coords = extract_raw_coords(in_path, reverse=Config.REVERSE_NEW_DATA)
        
        if coords is None or len(coords) < 10: continue
            
        # 2. 预测
        t_s, t_e = predictor.predict(coords)
        
        # 3. 保存 (传入是否反转了的标志，以便正确映射回原文件)
        save_labeled_vtk(in_path, out_path, t_s, t_e, reverse_applied=Config.REVERSE_NEW_DATA)
        
        count += 1
        if count % 10 == 0:
            print(f"   Processed {count}: {fname}")

if __name__ == "__main__":
    batch_inference()