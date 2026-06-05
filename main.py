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
    else:
        return obfuscate_core_math(target)

def ironbrew_wearedevs_pure_fixed(source_code):
    keys_count = random.randint(7, 12)
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
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[=[{fake_signature}:{hex_payload}]=]"
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_run = [random_var() for _ in range(3)]
    v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(4)]
    v_loop_k, v_matrix = random_var(), random_var()
    v_p_env, v_p_loader = random_var(), random_var()
    junk_pieces = []
    for _ in range(11000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top, junk_bottom = ";".join(junk_pieces[:half]), ";".join(junk_pieces[half:])
    matrix_elements = []
    for k_idx, k_val in enumerate(keys_list):
        matrix_elements.append(f"{{{obfuscate_core_math(k_val)},{obfuscate_core_math(k_idx + 3)}}}")
    matrix_elements.reverse() 
    lua_matrix_init = f"local {v_matrix} = {{{','.join(matrix_elements)}}};"
    
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
        f"local {v_buffer}=\"\"; "
        f"local h_clean=string.sub({v_bytecode},5); "
        f"{lua_matrix_init} "
        f"local v_byte_idx=0; "
        f"for {v_idx}=1,#h_clean,2 do "
        f"local {v_pair}=string.sub(h_clean,{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_num}; "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_dec}={v_bit_func}({v_dec},{v_matrix}[{v_loop_k}][1]); "
        f"end; "
        f"{v_buffer}={v_buffer}..string.char({v_dec}); "
        f"for {v_loop_k}=1,#{v_matrix} do "
        f"{v_matrix}[{v_loop_k}][1]=({v_matrix}[{v_loop_k}][1]+v_byte_idx+{v_matrix}[{v_loop_k}][2])%256; "
        f"end; "
        f"v_byte_idx=v_byte_idx+1; "
        f"end; "
        f"if type({v_p_loader}) == \"function\" then "
        f"local {v_run} = {v_p_loader}({v_buffer}); "
        f"if {v_run} then {v_run}() end "
        f"end"
    )
    total_payload = f"{junk_top};{bit_and_interpreter_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    loadstring_ascii = [108, 111, 97, 100, 115, 116, 114, 105, 110, 103]
    math_loadstring = [obfuscate_core_math(char) for char in loadstring_ascii]
    v_l_str, v_l_idx, v_l_val = random_var(), random_var(), random_var()
    gate_loadstring = (
        f"(function() "
        f"local {v_l_str} = \"\"; "
        f"for {v_l_idx}, {v_l_val} in ipairs({{{','.join(math_loadstring)}}}) do "
        f"{v_l_str} = {v_l_str} .. string.char({v_l_val}) "
        f"end; "
        f"return {v_l_str} "
        f"end)()"
    )
    execute_ascii = [101, 120, 101, 99, 117, 116, 101]
    math_execute = [obfuscate_core_math(char) for char in execute_ascii]
    v_e_str, v_e_idx, v_e_val = random_var(), random_var(), random_var()
    gate_execute = (
        f"(function() "
        f"local {v_e_str} = \"\"; "
        f"for {v_e_idx}, {v_e_val} in ipairs({{{','.join(math_execute)}}}) do "
        f"{v_e_str} = {v_e_str} .. string.char({v_e_val}) "
        f"end; "
        f"return {v_e_str} "
        f"end)()"
    )
    footer_args = (
        f"getfenv and getfenv() or _ENV, "
        f"loadstring or load or (getgenv and getgenv() or _G)[{gate_execute}] or (getgenv and getgenv() or _G)[{gate_loadstring}]"
    )
    clean_footer_args = " ".join(footer_args.splitlines()).strip()
    return f"-- This file was created by 8xms discord.gg/8mktK8HtT --\nreturn (function(...) return (function({v_p_env}, {v_p_loader}) {clean_payload} end)(...) end)({clean_footer_args})"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
    status_msg = await ctx.reply("Processing...")
    try:
        final_script = ironbrew_wearedevs_pure_fixed(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done", file=discord.File(file_stream, filename="message.txt"))
        await status_msg.delete()
    except Exception as e:
        if status_msg:
            await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
    
