import discord
from discord.ext import commands
import random
import string
import io
import re
import threading
import os
import base64
import hashlib
import time
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
    rest = ''.join(random.choices(string.ascii_letters + string.digits + "_", k=length-1))
    return first + rest

def random_var_lua():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    if random.random() > 0.5:
        return f"_{random.randint(0, 9)}{random.choice(chars)}"
    else:
        length = random.randint(2, 5)
        name = ''.join(random.choice(chars) for _ in range(length))
        if random.random() > 0.5:
            name += str(random.randint(0, 9))
        return name

def _math_add_sub(num):
    parts = []
    current = num
    for _ in range(3):
        val = random.randint(50, 500)
        if random.random() > 0.5:
            parts.append(f"+{val}")
            current -= val
        else:
            parts.append(f"-{val}")
            current += val
    return f"({current}{''.join(parts)})"

def _math_mul_div_safe(num):
    if num == 0:
        return _math_add_sub(0)
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    return f"(math.floor(({num}*{a})/{a})+{random.randint(10,50)}-{random.randint(10,50)})"

def _math_mixed_safe(num):
    a = random.randint(10, 50)
    b = random.randint(5, 20)
    c = random.randint(5, 30)
    product = (a + b) * c
    if product > num:
        return f"(({a}+{b})*{c}-{product - num})"
    else:
        return f"(({a}+{b})*{c}+{num - product})"

def _math_simple_safe(num):
    a = random.randint(10, 100)
    if random.random() > 0.5:
        return f"({num}+{a}-{a})"
    else:
        b = random.randint(2, 20)
        return f"(math.floor(({num}*{b})/{b}))"

def obfuscate_core_math_safe(target):
    target = abs(int(target))
    if target > 999999:
        target = target % 999999
    methods = [
        lambda: _math_add_sub(target),
        lambda: _math_mul_div_safe(target),
        lambda: _math_mixed_safe(target),
        lambda: _math_simple_safe(target)
    ]
    return random.choice(methods)()

def obfuscate_core_math(target):
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
    return f"({expr})".replace('\n', '').strip()

def generate_clean_advanced_junk(target):
    junk_mode = random.choice(['hex_ops_pool', 'negative_double', 'logical_inline', 'mixed_math_heavy', 'safe_math'])
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
        return f"({expr})".replace('\n', '').strip()
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
    elif junk_mode == 'safe_math':
        return _math_simple_safe(target)
    else:
        return obfuscate_core_math(target)

def base85_encode(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    padding = (4 - len(data) % 4) % 4
    data += b'\0' * padding
    result = []
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        n = int.from_bytes(chunk, 'big')
        chars = []
        for _ in range(5):
            chars.append(chr(33 + (n % 85)))
            n //= 85
        result.append(''.join(reversed(chars)))
    if padding:
        result[-1] = result[-1][:-padding]
    return ''.join(result)

def generate_anti_debug():
    v_check = random_var_lua()
    v_time = random_var_lua()
    v_result = random_var_lua()
    v_counter = random_var_lua()
    return f"""
    local function {v_check}()
        local {v_time} = os.clock()
        local {v_counter} = 0
        for i = 1, 100000 do
            {v_counter} = {v_counter} + 1
        end
        local {v_result} = os.clock() - {v_time}
        local debug_status = pcall(function()
            return debug and debug.getinfo and debug.getinfo(1)
        end)
        local is_roblox = pcall(function()
            return game and game.GetService
        end)
        local env_hash = 0
        for k, v in pairs(_G) do
            env_hash = (env_hash + type(v):byte(1) or 0) % 65521
        end
        if {v_result} > 1.5 or debug_status then
            return false
        end
        return true
    end
    if not {v_check}() then
        loadstring = function() return nil end
        pcall = function() return false end
        print = function() end
        getfenv = function() return {{}} end
        setmetatable = function() end
        getmetatable = function() return nil end
        _G = {{}}
        _ENV = {{}}
        return nil
    end
    """

def generate_control_flow_flattening(body_parts):
    v_state = random_var_lua()
    v_states = random_var_lua()
    v_func = random_var_lua()
    indices = list(range(len(body_parts)))
    random.shuffle(indices)
    states = []
    for idx in indices:
        states.append(f"[{idx}] = function() {body_parts[idx]} end")
    return f"""
    local {v_state} = 0
    local {v_states} = {{
        {','.join(states)}
    }}
    while {v_state} < #{v_states} do
        local {v_func} = {v_states}[{v_state} + 1]
        if {v_func} then
            {v_func}()
        end
        {v_state} = {v_state} + 1
        if {v_state} >= #{v_states} then
            break
        end
    end
    """

def generate_self_modifying():
    v_self = random_var_lua()
    v_key = random_var_lua()
    key_value = random.randint(50, 200)
    encrypted_self = key_value ^ 0x55
    return f"""
    local {v_self} = {encrypted_self}
    local {v_key} = 0x55
    {v_self} = ({v_self} ~ {v_key})
    if {v_self} ~= {key_value} then
        return nil
    end
    """

def generate_checksum(data):
    v_data = random_var_lua()
    v_a = random_var_lua()
    v_b = random_var_lua()
    v_i = random_var_lua()
    checksum_val = 1
    b_val = 0
    for byte in data.encode('utf-8'):
        checksum_val = (checksum_val + byte) % 65521
        b_val = (b_val + checksum_val) % 65521
    final_checksum = b_val * 65536 + checksum_val
    return f"""
    local function checksum_{v_data}({v_data})
        local {v_a} = 1
        local {v_b} = 0
        for {v_i} = 1, #{v_data} do
            {v_a} = ({v_a} + string.byte({v_data}, {v_i})) % 65521
            {v_b} = ({v_b} + {v_a}) % 65521
        end
        return {v_b} * 65536 + {v_a}
    end
    if checksum_{v_data}(decrypted) ~= {final_checksum} then
        for i = 1, 256 do _keys[i] = 0 end
        return nil
    end
    """

def generate_bitwise_interpreter():
    v_bit_func = random_var_lua()
    v_w = random_var_lua()
    v_m = random_var_lua()
    v_x = random_var_lua()
    v_i = random_var_lua()
    v_j = random_var_lua()
    v_res = random_var_lua()
    return f"""
    local function {v_bit_func}({v_i}, {v_j})
        if bit32 and bit32.bxor then
            return bit32.bxor({v_i}, {v_j})
        end
        local {v_x} = 0
        local {v_w} = 1
        local a = {v_i}
        local b = {v_j}
        while a > 0 or b > 0 do
            if (a % 2) ~= (b % 2) then
                {v_x} = {v_x} + {v_w}
            end
            a = math.floor(a / 2)
            b = math.floor(b / 2)
            {v_w} = {v_w} * 2
        end
        return {v_x}
    end
    """

def ironbrew_wearedevs_pure_fixed(source_code):
    keys_count = random.randint(12, 18)
    keys_list = [random.randint(50, 255) for _ in range(keys_count)]
    
    encrypted_hex_list = []
    current_keys = list(keys_list)
    for idx, byte in enumerate(source_code.encode('utf-8')):
        cipher_byte = byte
        for k in current_keys:
            cipher_byte = cipher_byte ^ k
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        for k_idx in range(len(current_keys)):
            current_keys[k_idx] = (current_keys[k_idx] + idx + (k_idx + 3)) % 256
    hex_payload = "".join(encrypted_hex_list)
    
    try:
        payload_bytes = bytes.fromhex(hex_payload)
        b85_payload = base85_encode(payload_bytes)
        use_b85 = True
    except:
        b85_payload = hex_payload
        use_b85 = False
    
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    if use_b85:
        bytecode_string_block = f"[=[B85:{fake_signature}:{b85_payload}]=]"
    else:
        bytecode_string_block = f"[=[{fake_signature}:{hex_payload}]=]"
    
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var_lua() for _ in range(7)]
    v_bytecode, v_buffer, v_run = [random_var_lua() for _ in range(3)]
    v_idx, v_pair, v_num, v_dec = [random_var_lua() for _ in range(4)]
    v_loop_k, v_matrix = random_var_lua(), random_var_lua()
    v_p_env, v_p_loader = random_var_lua(), random_var_lua()
    
    junk_pieces = []
    used_names = set()
    for _ in range(8000):
        v_junk = random_var_lua()
        while v_junk in used_names:
            v_junk = random_var_lua()
        used_names.add(v_junk)
        rand_target = random.randint(50, 99999)
        if random.random() < 0.2 and len(junk_pieces) > 10:
            prev_junk = random.choice(list(used_names))
            junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}; {prev_junk} = {prev_junk} + {v_junk}")
        else:
            junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    
    half = len(junk_pieces) // 2
    junk_top = ";".join(junk_pieces[:half])
    junk_bottom = ";".join(junk_pieces[half:])
    
    matrix_elements = []
    for k_idx, k_val in enumerate(keys_list):
        matrix_elements.append(f"{{{obfuscate_core_math(k_val)},{obfuscate_core_math(k_idx + 3)}}}")
    matrix_elements.reverse()
    lua_matrix_init = f"local {v_matrix} = {{{','.join(matrix_elements)}}};"
    
    bit_and_interpreter_core = f"""
        {generate_bitwise_interpreter()}
        local {v_bytecode} = {bytecode_string_block};
        local {v_buffer} = "";
        local h_clean = string.sub({v_bytecode}, 5);
        {lua_matrix_init}
        local v_byte_idx = 0;
        local payload = h_clean
        if string.sub(h_clean, 1, 4) == "B85:" then
            payload = string.sub(h_clean, 5)
        end
        for {v_idx} = 1, #payload, 2 do
            local {v_pair} = string.sub(payload, {v_idx}, {v_idx} + 1);
            local {v_num} = tonumber({v_pair}, 16);
            local {v_dec} = {v_num};
            for {v_loop_k} = 1, #{v_matrix} do
                {v_dec} = {v_bit_func}({v_dec}, {v_matrix}[{v_loop_k}][1]);
            end;
            {v_buffer} = {v_buffer} .. string.char({v_dec});
            for {v_loop_k} = 1, #{v_matrix} do
                {v_matrix}[{v_loop_k}][1] = ({v_matrix}[{v_loop_k}][1] + v_byte_idx + {v_matrix}[{v_loop_k}][2]) % 256;
            end;
            v_byte_idx = v_byte_idx + 1;
        end;
        {generate_anti_debug()}
        {generate_self_modifying()}
        {generate_checksum(source_code)}
        if type({v_p_loader}) == "function" then
            local {v_run} = {v_p_loader}({v_buffer});
            if {v_run} then
                {v_run}()
            end
        end
    """
    
    code_parts = bit_and_interpreter_core.split(';')
    chunks = []
    chunk_size = max(3, len(code_parts) // 5)
    for i in range(0, len(code_parts), chunk_size):
        chunk = ';'.join(code_parts[i:i+chunk_size])
        chunks.append(chunk)
    
    flattened_code = generate_control_flow_flattening(chunks)
    
    total_payload = f"{junk_top};{flattened_code};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    
    # NÉN THÀNH 1 DÒNG
    clean_payload = clean_payload.replace('\n', '').replace('  ', ' ').strip()
    
    loadstring_ascii = [108, 111, 97, 100, 115, 116, 114, 105, 110, 103]
    math_loadstring = [obfuscate_core_math(char) for char in loadstring_ascii]
    v_l_str, v_l_idx, v_l_val = random_var_lua(), random_var_lua(), random_var_lua()
    gate_loadstring = f"""
        (function()
            local {v_l_str} = "";
            for {v_l_idx}, {v_l_val} in ipairs({{{','.join(math_loadstring)}}}) do
                {v_l_str} = {v_l_str} .. string.char({v_l_val})
            end;
            return {v_l_str}
        end)()
    """
    
    execute_ascii = [101, 120, 101, 99, 117, 116, 101]
    math_execute = [obfuscate_core_math(char) for char in execute_ascii]
    v_e_str, v_e_idx, v_e_val = random_var_lua(), random_var_lua(), random_var_lua()
    gate_execute = f"""
        (function()
            local {v_e_str} = "";
            for {v_e_idx}, {v_e_val} in ipairs({{{','.join(math_execute)}}}) do
                {v_e_str} = {v_e_str} .. string.char({v_e_val})
            end;
            return {v_e_str}
        end)()
    """
    
    footer_args = f"""
        getfenv and getfenv() or _ENV,
        loadstring or load or 
        (getgenv and getgenv() or _G)[{gate_execute}] or 
        (getgenv and getgenv() or _G)[{gate_loadstring}] or
        (rawget(_G, {gate_loadstring})) or
        (rawget(_G, {gate_execute}))
    """
    clean_footer_args = " ".join(footer_args.splitlines()).strip()
    
    return f"""-- This file is protected by Advanced Lua Obfuscator v3.0
-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
-- Lua 5.1 Compatible

return (function(...) 
    return (function({v_p_env}, {v_p_loader}) 
        {clean_payload} 
    end)(...) 
end)({clean_footer_args})"""

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    
    if not source_code or not source_code.strip():
        return await ctx.reply("Please provide code or attach a .lua file.")
    
    if len(source_code) > 100000:
        return await ctx.reply("Code too large (max 100KB)")
    
    status_msg = await ctx.reply("Processing...")
    
    try:
        start_time = time.time()
        final_script = ironbrew_wearedevs_pure_fixed(source_code)
        elapsed = time.time() - start_time
        
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        
        await ctx.send(
            content=f"{ctx.author.mention} Done!\n"
                    f"Size: {(len(final_script)/1024):.2f}KB\n"
                    f"Time: {elapsed:.2f}s",
            file=discord.File(file_stream, filename="obfuscated.lua")
        )
        await status_msg.delete()
        
    except Exception as e:
        if status_msg:
            await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
