import discord
from discord.ext import commands
import random
import string
import io
import re
import threading
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live"

def run_server():
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

def random_var(length=6):
    first = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))
    return first + rest

def obfuscate_core_math(target):
    """
    """
    current_val = target
    ops_pool = []
    for _ in range(random.randint(2, 3)):
        op = random.choice(['+', '-'])
        rand_num = random.randint(100000, 500000)
        if op == '+':
            current_val = current_val - rand_num
            ops_pool.append(f"+{hex(rand_num)}" if random.choice([True, False]) else f"+{rand_num}")
        elif op == '-':
            current_val = current_val + rand_num
            ops_pool.append(f"-{hex(rand_num)}" if random.choice([True, False]) else f"-{rand_num}")
    start_style = random.choice(['normal', 'hex'])
    expr = hex(current_val) if start_style == 'hex' else str(current_val)
    for action in reversed(ops_pool):
        expr = f"({expr}{action})"
    return f"({expr})"

def generate_clean_advanced_junk(target):
    """
    """
    junk_mode = random.choice(['hex_ops_pool', 'negative_double', 'logical_inline', 'mixed_math_heavy'])
    
    if junk_mode == 'hex_ops_pool':
        current_val = target
        ops_pool = []
        for _ in range(random.randint(2, 4)):
            op = random.choice(['+', '-'])
            rand_num = random.randint(100000, 1500000)
            if op == '+':
                current_val -= rand_num
                ops_pool.append(f"+{hex(rand_num)}")
            else:
                current_val += rand_num
                ops_pool.append(f"-{hex(rand_num)}")
        expr = hex(current_val)
        for action in reversed(ops_pool):
            expr = f"({expr}{action})"
        return f"({expr})"
        
    elif junk_mode == 'negative_double':
        offset1 = random.randint(50000, 200000)
        offset2 = random.randint(10000, 40000)
        base = target + offset1 - offset2
        return f"(-(-{base}-{hex(offset1)})+{hex(offset2)})"
        
    elif junk_mode == 'logical_inline':
        rand_check = random.randint(100, 1000)
        rand_adder = random.randint(5000, 15000)
        if random.choice([True, False]):
            return f"({target - rand_adder} + ({rand_check} > 50 and {rand_adder} or 0))"
        else:
            return f"({target + rand_adder} - ({rand_check} < 50 and 0 or {rand_adder}))"
            
    else:
        return obfuscate_core_math(target)

def ironbrew_total_wrapped_v12_1(source_code):
    # Thiết lập số lượng tầng khóa ngẫu nhiên từ 7 đến 12 tầng độc lập
    keys_count = random.randint(7, 12)
    keys_list = [random.randint(50, 255) for _ in range(keys_count)]
    
    # Mã hóa Payload nguồn qua hệ thống Multi-Key Layer liên hoàn kết hợp khóa cuộn
    encrypted_hex_list = []
    current_keys = list(keys_list)
    
    for idx, byte in enumerate(source_code.encode('utf-8')):
        cipher_byte = byte
        # XOR xuôi dòng qua toàn bộ các lớp khóa
        for k in current_keys:
            cipher_byte = cipher_byte ^ k
            
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        
        # Cuộn độc lập từng khóa với bước dịch (k_idx + 3)
        for k_idx in range(len(current_keys)):
            current_keys[k_idx] = (current_keys[k_idx] + idx + (k_idx + 3)) % 256

    hex_payload = "".join(encrypted_hex_list)
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[=[{fake_signature}:{hex_payload}]=]"
    
    # Sử dụng cặp key đầu và cuối để mã hóa chuỗi hệ thống "loadstring" và "load"
    hex_loadstring = "".join([f"{ord(c) ^ keys_list[0] ^ keys_list[-1]:02X}" for c in "loadstring"])
    hex_load = "".join([f"{ord(c) ^ keys_list[0] ^ keys_list[-1]:02X}" for c in "load"])
    len_ls, len_l = len(hex_loadstring), len(hex_load)
    
    # Sinh tên biến ngẫu nhiên cho VM Lua
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_func, v_run = [random_var() for _ in range(4)]
    v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(4)]
    v_loop_idx, v_env = random_var(), random_var()
    v_str1, v_str2, v_t_idx, v_t_pair = [random_var() for _ in range(4)]
    v_h_ls, v_h_l = random_var(), random_var()
    v_byte_idx = random_var()
    
    # Các biến cấu trúc mảng khóa mới
    v_matrix, v_k_step, v_loop_k = random_var(), random_var(), random_var()

    # Sinh 2500 dòng biến rác đa dạng thể loại bao bọc ngoài rìa
    junk_pieces = []
    for _ in range(10000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top, junk_bottom = ";".join(junk_pieces[:half]), ";".join(junk_pieces[half:])
    
    # Đóng gói toàn bộ các Key thực và Hằng số cuộn vào cấu trúc Table ẩn danh
    matrix_elements = []
    for k_idx, k_val in enumerate(keys_list):
        obf_val = obfuscate_core_math(k_val)
        obf_offset = obfuscate_core_math(k_idx + 3)
        matrix_elements.append(f"{{{obf_val},{obf_offset}}}")
        
    # Đảo ngược mảng phần tử để vòng lặp giải mã duyệt từ 1 đến #mảng một cách tự nhiên (giải mã ngược thứ tự lúc mã hóa)
    matrix_elements.reverse() 
    
    # ĐÃ FIX: Sửa dấu đóng mở ngoặc chính xác tránh lỗi cú pháp trong Lua sinh ra
    lua_matrix_init = f"local {v_matrix} = {{{','.join(matrix_elements)}}};"

    # Lõi trình thông dịch VM v12.1 sử dụng vòng lặp kín chống đếm dòng
    bit_and_interpreter_core = (
        f"local function {v_bit_func}({v_i},{v_j}) "
        f"local {v_x}=0; "
        f"for {v_m}=0,7 do "
        f"local {v_w}=({v_i}/({obfuscate_core_math(2)})^{v_m})%2; "
        f"local {v_res}=({v_j}/({obfuscate_core_math(2)})^{v_m})%2; "
        f"if {v_w}-{v_w}%1~={v_res}-{v_res}%1 then {v_x}={v_x}+({obfuscate_core_math(2)})^{v_m} end "
        f"end "
        f"return {v_x} "
        f"end; "
        f"local {v_bytecode}={bytecode_string_block}; "
        f"local {v_h_ls}=\"{hex_loadstring}\"; "
        f"local {v_h_l}=\"{hex_load}\"; "
        f"local {v_buffer}=\"\"; "
        f"for {v_loop_idx}={obfuscate_core_math(1)},{obfuscate_core_math(2)} do "
        f"if {v_loop_idx}=={obfuscate_core_math(1)} then "
        f"local h_clean=string.sub({v_bytecode},5); "
        f"{lua_matrix_init} " # Nạp ma trận khóa đã sửa cú pháp chuẩn
        f"local {v_byte_idx}=0; "
        f"for {v_idx}=1,#h_clean,2 do "
        f"local {v_pair}=string.sub(h_clean,{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_num}; "
        
        # VÒNG LẶP GIẢI MÃ KÍN: Chỉ có ĐÚNG 1 dòng gọi hàm giải mã XOR trơ trọi!
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_dec}={v_bit_func}({v_dec},{v_matrix}[{v_loop_k}][1]); "
        f"end; "
        
        f"{v_buffer}={v_buffer}..string.char({v_dec}); "
        
        # VÒNG LẶP CUỘN KHÓA KÍN: Tự động cuộn toàn bộ mảng khóa đồng bộ
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_matrix}[{v_loop_k}][1]=({v_matrix}[{v_loop_k}][1]+{v_byte_idx}+{v_matrix}[{v_loop_k}][2])%256; "
        f"end; "
        
        f"{v_byte_idx}={v_byte_idx}+1; "
        f"end "
        f"elseif {v_loop_idx}=={obfuscate_core_math(2)} then "
        f"local {v_str1}, {v_str2} = \"\", \"\"; "
        f"{lua_matrix_init} "
        f"local {v_k_step}={v_bit_func}({v_matrix}[#{v_matrix}][1],{v_matrix}[1][1]); "
        f"for {v_t_idx}=1,{obfuscate_core_math(len_ls)},2 do "
        f"local {v_t_pair}=string.sub({v_h_ls},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then {v_str1}={v_str1}..string.char({v_bit_func}(tonumber({v_t_pair},16),{v_k_step})) end "
        f"end; "
        f"for {v_t_idx}=1,{obfuscate_core_math(len_l)},2 do "
        f"local {v_t_pair}=string.sub({v_h_l},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then {v_str2}={v_str2}..string.char({v_bit_func}(tonumber({v_t_pair},16),{v_k_step})) end "
        f"end; "
        f"local {v_env}=getfenv(); "
        f"local {v_func}={v_env}[{v_str1}] or {v_env}[{v_str2}]; "
        f"local {v_run}={v_func}({v_buffer}); "
        f"if {v_run} then {v_run}(...) end "
        f"end "
        f"end"
    )
    
    total_payload = f"{junk_top};{bit_and_interpreter_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    return f"-- This file was created by 8xms discord.gg/8mktK8HtT --\nreturn(function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
    status_msg = await ctx.reply("<a:loading:1477881141678702603> Processing ")
    try:
        final_script = ironbrew_total_wrapped_v12_1(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done", file=discord.File(file_stream, filename="message.txt"))
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
    
