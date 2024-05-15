import open3d as o3d

bin_file_path = r"C:\Users\H_\Desktop\Sungmin_Github\LIDAR_practice\000000.pcd"

### outlier 제거
# 1.Statistical Outlier Removal
# "neighbor"라는 단위로 group을 묶은 다음, point cloud들 간의 "distance" 기준 평균과 표준 편차를 구하고, "std_ratio"라는 threshold 값을 설정하여 "거리의 편차"가 큰 point cloud를 outlier로 정의한다. -> Z-score와 매우 유사하다(표준 정규 분포)
#  parameter로는 nb_neighbors : group을 묶을 개수, std_ratio : threshold
# Z-score의 방식과 유사하다.
def statistical_rm_outlier():
    pcd = o3d.io.read_point_cloud(bin_file_path)
    downsampled_pcd = pcd.voxel_down_sample(voxel_size = 0.5)
    
    rm_outlier_pcd, inliers = downsampled_pcd.remove_statistical_outlier(nb_neighbors = 20, std_ratio = 2.0)

    inliers_cloud_index = rm_outlier_pcd.select_by_index(inliers, invert = False) 
    outliers_cloud_index = rm_outlier_pcd.select_by_index(inliers, invert = True) 

    inliers_cloud_index.paint_uniform_color([0.5, 0.5, 0.5]) # RGB순서
    outliers_cloud_index.paint_uniform_color([1, 0, 0]) 

    o3d.visualization.draw_geometries([inliers_cloud_index, outliers_cloud_index])

# 2. Radius Outlier Removal
# 구(sphere)를 그리고, 구 내부에 point cloud의 개수가 일정 개수 이하만 있으면 outlier로 제거하는 방식이다.
# 듬성 듬성 존재하는 점들을 제거하기 좋은 방법이라고 한다.
# parameter : nb_points : 구 안에 nb_points 이하의 point cloud가 존재하면 outlier로 정할 수 있는 threshold, radius : 구의 반지름(단위 : meter) 크기가 커지면 계산량 많아짐
def radius_rm_outlier():
    pcd = o3d.io.read_point_cloud(bin_file_path)
    print(len(pcd.points))
    downsampled_pcd = pcd.voxel_down_sample(voxel_size = 0.3)

    rm_outlier_pcd, inliers = downsampled_pcd.remove_radius_outlier(nb_points = 20, radius = 0.5)
   
    inliers_cloud_index = rm_outlier_pcd.select_by_index(inliers, invert = False) 
    outliers_cloud_index = rm_outlier_pcd.select_by_index(inliers, invert = True) 

    inliers_cloud_index.paint_uniform_color([0.5, 0.5, 0.5]) # RGB순서
    outliers_cloud_index.paint_uniform_color([1, 0, 0]) 

    o3d.visualization.draw_geometries([inliers_cloud_index, outliers_cloud_index], width = 640, height = 480)  
