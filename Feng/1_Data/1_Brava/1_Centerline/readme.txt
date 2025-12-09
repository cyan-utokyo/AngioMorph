1：原始的资料集（from Chen），vtk 格式，resampling成180个点,不等距，只有坐标信息，无半径信息 (vtk)

2：无更改，应该就是copy了一份 (vtk)

3：把中心线2的出入口延长12和22mm，点的数量resampling成300 (vtk)
    D:\github\Phd_summary\2_Code\1_Brava\1_Preprocessing\1_Centerline_Preprocessing.ipynb

4：把中心线3加上半径信息R=1mm (vtk)
    D:\github\Phd_summary\2_Code\1_Brava\1_Preprocessing\1_Centerline_Preprocessing.ipynb
    
5：中心线4的变形。网格变形用，只有坐标信息的300点 (txt)
    D:\github\Phd_summary\2_Code\1_Brava\1_Preprocessing\1_Centerline_Preprocessing.ipynb

6：把中心线5用V-modeler计算的曲率和扭率 (ply)

7：利用中心线6抽取出siphon部位(vtk)
    D:\github\Phd_summary\2_Code\1_Brava\1_Preprocessing\1_Centerline_Preprocessing.ipynb

8：把中心线7用标签分成B1 B2两个部分(vtk)
    D:\github\Phd_summary\2_Code\1_Brava\1_Preprocessing\2_Centerline_Siphon_Preprocessing.ipynb