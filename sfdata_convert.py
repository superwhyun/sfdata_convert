import yaml, json
import random
import bitstring


role2type_dic = {
    "sensor":1,
    "actuator":2
}

func2code_dic = {
    "temperature":1, 
    "humidity":7, 
    "CO2":32,
    "pyranometer":11,
    "winddirection":8,
    "windspeed":9,
    "rain":28,
    "quantum":16,
    "soilmoisture":29,
    "soiltension":22,
    "EC":24,
    "PH":25,
    "soiltemperature": 18,
    "uppermotor": 1,
    "sidemotor" : 2,
    "warmmotor" : 11,
    "curtainmotor" : 6,
    "ventilationfan" : 3,
    "circulationfan" : 12,
    "irrigationpump" : 8,
    "irrigationvalve" : 13,
    "coolingheater" : 4    
    }

# actuator2code_dic = {
#     "uppermotor": 1,
#     "sidemotor" : 2,
#     "warmmotor" : 11,
#     "curtainmotor" : 6,
#     "ventilationfan" : 3,
#     "circulationfan" : 12,
#     "irrigationpump" : 8,
#     "irrigationvalve" : 13,
#     "coolingheater" : 4
# }


unit2code_dic = {
    "none":0,
    "default":1,
    "celsius":2,
    "fahrenheit":3,
    "percentage":4,
    "ppm":5,
    "W/m2":6,
    "degree":7,
    "m/s":8,
    "umol/m2s":9,
    "%vol":10,
    "kPa":11,
    "dS/m":12,
    "pH":13
}

def gen_rand_values(conf, dtype, identifier):

    if(conf is None):
        print("error: argument error")
        return
    
    if(identifier ==-1):
        identifier = random.randint(0, 127)

    data=conf[dtype]
    if(data["value"]["type"] != 3):
        value = random.randint(data["value"]["min"], data["value"]["max"])
    else:
        value = random.uniform(data["value"]["min"], data["value"]["max"])
        value = round(value,int(data["value"]["precision"]))

    D = dict()
    D1 = dict()
    D1['identifier']=identifier
    D1['type']=data["type"]
    D1['code']=data["code"]
    D1['value']=value
    D1['unit']=data["value"]["unit"]
    D1['precision']=data["value"]["precision"]

    D[dtype]=D1

    return D


def gen_bitstring(val, len):

    if( type(val) == int ):
        genbit = bitstring.BitArray(int=val, length=len*8)
    else:
        genbit = bitstring.BitArray(float=val, length=len*8)

    return "0x"+genbit.hex+" ==> "+genbit.bin


def gen_binary_values(conf, dval):
    D = dict()

    D["identifier"] = gen_bitstring(dval["identifier"], conf["identifier"])
    D["type"] = gen_bitstring(role2type_dic[dval["type"]], conf["type"])
    D["code"] = gen_bitstring(func2code_dic[dval["code"]], conf["code"])
    D["length"] = gen_bitstring(conf["value"], conf["length"])
    D["value"] = gen_bitstring(dval["value"], conf["value"])
    D["unit"] = gen_bitstring(unit2code_dic[dval["unit"]], conf["unit"])


    # TLV 파라미터가 필요한 경우 (drafting...)
    # attr_cnt=0
    # for attr in conf["attr"]:
    #     if(attr == "unit"): 
    #         D["unit"] = gen_bitstring(unit2code_dic[value["unit"]], 1)
    #         attr_cnt = attr_cnt+1
        

    return D


stream = open('sfdata_cfg.yml','r')
            


# print("-----------------YAML-----------------");
yaml_dict = yaml.load(stream)
# print (yaml_dict)

# print("-----------------JSON-----------------");
# print (json.dumps(yaml_dict, sort_keys=False, indent=2))

value_list = [
    "temperature",
    "humidity",
    "CO2",
    "pyranometer",
    "winddirection",
    "windspeed",
    "rain",
    "quantum",
    "soilmoisture",
    "soiltension",
    "EC",
    "PH",
    "soiltemperature",
    "uppermotor",
    "sidemotor",
    "warmmotor",
    "curtainmotor",
    "ventilationfan",
    "circulationfan",
    "irrigationpump",
    "irrigationvalve",
    "coolingheater"
    
]




for val_type in value_list:
    # val_type = "temperature"
    print("--------------[", val_type , "]-----------")
    rand_val = gen_rand_values(yaml_dict, val_type, -1)
    binary_val = gen_binary_values(yaml_dict[val_type]["binary"], rand_val[val_type])

    print("[JSON]\n", json.dumps(rand_val, indent=2))
    print("[Binary]\n", json.dumps(binary_val, indent=2))


