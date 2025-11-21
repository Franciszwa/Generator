# By AbdeeLkarim BesTo

import requests , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading , random , os , asyncio
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Key , Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]) , bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

async def EnC_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
    
async def DEc_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()
    
async def EnC_PacKeT(HeX , K , V): 
    return AES.new(K , AES.MODE_CBC , V).encrypt(pad(bytes.fromhex(HeX) ,16)).hex()
    
async def DEc_PacKeT(HeX , K , V):
    return unpad(AES.new(K , AES.MODE_CBC , V).decrypt(bytes.fromhex(HeX)) , 16).hex()  

async def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

async def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)
    
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n
    
async def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return await EnC_Vr(field_header) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return await EnC_Vr(field_header) + await EnC_Vr(len(encoded_value)) + encoded_value

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await CrEaTe_ProTo(value)
            packet.extend(await CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet
    
async def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    if len(F) == 1: F = "0" + F
    return F

async def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type in ["varint", "string", "bytes"]:
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = await Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

async def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_dict = await Fix_PackEt(parsed_results.results)
        return json.dumps(parsed_results_dict)
    except Exception as e:
        print(f"error decoding packet: {e}")
        return None
                      
def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 3] for i in range(0 , len(str(n)) , 3))
    
async def Ua():
    versions = ['4.0.18P6', '4.1.5P2', '5.0.2P4', '5.5.2P3']
    models = ['SM-A515F', 'Redmi 9A', 'POCO M3', 'RMX3085', 'moto g(9) play']
    android_versions = ['10', '11', '12', '13']
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {random.choice(android_versions)};en;IND;)"
    
async def ArA_CoLor():
    Tp = ["32CD32" , "00BFFF" , "FF4500" , "FFD700" , "6A5ACD" , "FF8C00" , "FFA07A"]
    return random.choice(Tp)
    
async def xBunnEr():
    bN = [902000126 , 902000154 , 902048021 , 902000027 , 902000078, 902033016]
    return random.choice(bN)

async def xSEndMsg(Msg , Tp , Tp2 , id , K , V):
    feilds = {1: id , 2: Tp2 , 3: Tp, 4: Msg, 5: int(time.time()), 9: {1: "SHAZZ", 2: int(await xBunnEr()), 4: 330}, 10: "en"}
    Pk = (await CrEaTe_ProTo(feilds)).hex()
    Pk = "080112" + (await EnC_Vr(len(Pk) // 2)).hex() + Pk
    return await GeneRaTePk(Pk, '1201', K, V)
    
async def xSEndMsgsQ(Msg , id , K , V):
    fields = {1: id , 2: id , 4: Msg , 5: int(time.time()), 9: {1: "SHAZZ", 2: await xBunnEr(), 4: 330}, 10: "en"}
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + (await EnC_Vr(len(Pk) // 2)).hex() + Pk
    return await GeneRaTePk(Pk, '1201', K, V)     

async def AuthClan(CLan_Uid, AuTh, K, V):
    fields = {1: 3, 2: {1: int(CLan_Uid), 2: 1, 4: str(AuTh)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1201' , K , V)

async def GenJoinSquadsPacket(code,  K , V):
    fields = {1: 4, 2: {5: str(code), 6: 6}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)   

async def Emote_k(TarGeT , idT, K, V,region):
    fields = {1: 21, 2: {1: 804266360, 2: 909000001, 5: {1: TarGeT, 3: idT}}}
    packet_header = "0515"
    if region.lower() == "ind": packet_header = '0514'
    elif region.lower() == "bd": packet_header = "0519"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet_header , K , V)

async def GeTSQDaTa(D):
    uid = D['5']['data']['1']['data']
    chat_code = D["5"]["data"]["14"]["data"]
    squad_code = D["5"]["data"]["31"]["data"]
    return uid, chat_code , squad_code

async def AutH_Chat(T , uid, code, region, K, V):
    fields = {1: T, 2: {1: uid, 2: region, 3: "en", 4: str(code)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '1215' , K , V)

async def GeneRaTePk(Pk , N , K , V):
    PkEnc = await EnC_PacKeT(Pk , K , V)
    _ = await DecodE_HeX(int(len(PkEnc) // 2))
    header_len = len(_)
    if header_len <= 2: HeadEr = N + "000000"
    elif header_len == 3: HeadEr = N + "00000"
    elif header_len == 4: HeadEr = N + "0000"
    else: HeadEr = N + "000"
    return bytes.fromhex(HeadEr + _ + PkEnc)

async def OpEnSq(K , V,region):
    fields = {1: 1, 2: {2: "\u0001", 3: 1, 4: 1, 5: "en", 9: 1, 11: 1, 13: 1, 14: {2: 5756, 6: 11, 8: "1.118.1", 9: 2, 10: 4}}}
    packet_header = "0515"
    if region.lower() == "ind": packet_header = '0514'
    elif region.lower() == "bd": packet_header = "0519"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet_header , K , V)

async def cHSq(Nu , Uid , K , V,region):
    fields = {1: 17, 2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}}
    packet_header = "0515"
    if region.lower() == "ind": packet_header = '0514'
    elif region.lower() == "bd": packet_header = "0519"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet_header , K , V)

async def SEnd_InV(Nu , Uid , K , V,region):
    fields = {1: 2 , 2: {1: int(Uid) , 2: region , 4: int(Nu)}}
    packet_header = "0515"
    if region.lower() == "ind": packet_header = '0514'
    elif region.lower() == "bd": packet_header = "0519"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , packet_header , K , V)

async def ExiT(idT , K , V):
    fields = {1: 7}
    if idT:
        fields[2] = {1: idT}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)