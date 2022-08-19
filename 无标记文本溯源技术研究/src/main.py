from Decode import DecodeModule
from Encode import EncodeModule

txt_path = "../datas/before.txt"
num = 25
num_length = 7
serial_length = 15
dic_paths = ["../datas/dics/0.txt", 
             "../datas/dics/1.txt",
             "../datas/dics/2.txt", 
             "../datas/dics/3.txt",]
out_path = "../datas/after.txt"

module_encode = EncodeModule()
module_encode.Load(txt_path, num, num_length, dic_paths)
module_encode.InsertWatermark(out_path)


module_decode = DecodeModule()
module_decode.Load(out_path, serial_length, dic_paths)
result = module_decode.Check()
module_decode.Evaluate(result)
