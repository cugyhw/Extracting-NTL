import pandas as pd
from osgeo import gdal

# 读取CSV文件
csv_file = r'D:\Features_NTL.csv'
df = pd.read_csv(csv_file)

# 读取TIF文件
tif_file = 'D:\NTL_WuHan_2019-2020.tif'
dataset = gdal.Open(tif_file)
band = dataset.GetRasterBand(1)

# 获取TIF文件的栅格信息
geotransform = dataset.GetGeoTransform()
x_origin = geotransform[0]
y_origin = geotransform[3]
pixel_width = geotransform[1]
pixel_height = geotransform[5]

# 遍历CSV文件的每一行记录
for index, row in df.iterrows():
    # 获取经纬度坐标
    longitude = row['querylon']
    latitude = row['querylat']
    
    # 计算栅格坐标
    x_offset = int((longitude - x_origin) / pixel_width)
    y_offset = int((latitude - y_origin) / pixel_height)
    
    # 读取对应栅格的DN值
    dn_value = band.ReadAsArray(x_offset, y_offset, 1, 1)[0][0]
    
    # 将DN值添加到CSV文件的最后一列
    df.at[index, 'NTL_DN'] = dn_value

# 保存修改后的CSV文件
output_csv_file = r'D:\Features_NTL.csv'
df.to_csv(output_csv_file, index=False)