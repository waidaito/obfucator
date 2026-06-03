import discord
from discord.ext import commands
import random
import string
import io
import re
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live"

def run_server():
    app.run(host='0.0.0.0', port=8080)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

def random_var(length=6):
    first = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))
    return first + rest

def obfuscate_to_mixed_math(target):
    current_val = target
    ops_pool = []
    
    for _ in range(random.randint(2, 4)):
        op = random.choice(['+', '-'])
        rand_num = random.randint(100000, 1500000)
        
        if op == '+':
            current_val = current_val - rand_num
            display_style = random.choice(['normal', 'negative', 'hex'])
            if display_style == 'normal':
                ops_pool.append(f"+{rand_num}")
            elif display_style == 'negative':
                ops_pool.append(f"-(-{rand_num})")
            else:
                ops_pool.append(f"+{hex(rand_num)}")
        elif op == '-':
            current_val = current_val + rand_num
            display_style = random.choice(['normal', 'negative', 'hex'])
            if display_style == 'normal':
                ops_pool.append(f"-{rand_num}")
            elif display_style == 'negative':
                ops_pool.append(f"+(-{rand_num})")
            else:
                ops_pool.append(f"-{hex(rand_num)}")
            
    start_style = random.choice(['normal', 'hex'])
    expr = hex(current_val) if start_style == 'hex' else str(current_val)
    
    for action in reversed(ops_pool):
        expr = f"({expr}{action})"
    return f"({expr})"

def ironbrew_total_wrapped_v10_6(source_code):
    secret_key = random.randint(100, 250)
    
    encrypted_hex_list = []
    for byte in source_code.encode('utf-8'):
        cipher_byte = byte ^ secret_key
        encrypted_hex_list.append(f"{cipher_byte:02X}")
        
    hex_payload = "".join(encrypted_hex_list)
    fake_signature = "".join(random.choices(string.ascii_uppercase, k=3))
    bytecode_string_block = f"[=[{fake_signature}:{hex_payload}]=]"
    
    hex_loadstring = "".join([f"{ord(c) ^ secret_key:02X}" for c in "loadstring"])
    hex_load = "".join([f"{ord(c) ^ secret_key:02X}" for c in "load"])
    
    len_ls = len(hex_loadstring)
    len_l = len(hex_load)
    
    v_bit_func, v_w, v_m, v_x, v_i, v_j, v_res = [random_var() for _ in range(7)]
    v_bytecode, v_buffer, v_func, v_run = [random_var() for _ in range(4)]
    v_idx, v_pair, v_num, v_dec = [random_var() for _ in range(4)]
    v_loop_idx, v_env = random_var(), random_var()
    
    v_str1, v_str2, v_t_idx, v_t_pair = [random_var() for _ in range(4)]
    v_h_ls, v_h_l = random_var(), random_var()

    junk_pieces = []
    for _ in range(2000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={obfuscate_to_mixed_math(rand_target)}")
        
    half = len(junk_pieces) // 2
    junk_top = ";".join(junk_pieces[:half])
    junk_bottom = ";".join(junk_pieces[half:])

    bit_and_interpreter_core = (
        f"local function {v_bit_func}({v_i},{v_j}) "
        f"local {v_x}=0; "
        f"for {v_m}=0,7 do "
        f"local {v_w}=({v_i}/{obfuscate_to_mixed_math(2)}^{v_m})%2; "
        f"local {v_res}=({v_j}/{obfuscate_to_mixed_math(2)}^{v_m})%2; "
        f"if {v_w}-{v_w}%1~={v_res}-{v_res}%1 then "
        f"{v_x}={v_x}+{obfuscate_to_mixed_math(2)}^{v_m} "
        f"end "
        f"end "
        f"return {v_x} "
        f"end; "
        f"local {v_bytecode}={bytecode_string_block}; "
        f"local {v_h_ls}=\"{hex_loadstring}\"; "
        f"local {v_h_l}=\"{hex_load}\"; "
        f"local {v_buffer}=\"\"; "
        f"for {v_loop_idx}={obfuscate_to_mixed_math(1)},{obfuscate_to_mixed_math(2)} do "
        f"if {v_loop_idx}=={obfuscate_to_mixed_math(1)} then "
        f"local h_clean=string.sub({v_bytecode},5); "
        f"for {v_idx}=1,#h_clean,2 do "
        f"local {v_pair}=string.sub(h_clean,{v_idx},{v_idx}+1); "
        f"local {v_num}=tonumber({v_pair},16); "
        f"local {v_dec}={v_bit_func}({v_num},{obfuscate_to_mixed_math(secret_key)}); "
        f"{v_buffer}={v_buffer}..string.char({v_dec}) "
        f"end "
        f"elseif {v_loop_idx}=={obfuscate_to_mixed_math(2)} then "
        f"local {v_str1}, {v_str2} = \"\", \"\"; "
        f"for {v_t_idx}=1,{obfuscate_to_mixed_math(len_ls)},2 do "
        f"local {v_t_pair}=string.sub({v_h_ls},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then "
        f"{v_str1}={v_str1}..string.char({v_bit_func}(tonumber({v_t_pair},16),{obfuscate_to_mixed_math(secret_key)})) "
        f"end "
        f"end; "
        f"for {v_t_idx}=1,{obfuscate_to_mixed_math(len_l)},2 do "
        f"local {v_t_pair}=string.sub({v_h_l},{v_t_idx},{v_t_idx}+1); "
        f"if #{v_t_pair}==2 then "
        f"{v_str2}={v_str2}..string.char({v_bit_func}(tonumber({v_t_pair},16),{obfuscate_to_mixed_math(secret_key)})) "
        f"end "
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

def is_valid_lua(source_code):
    if len(source_code.strip()) < 10:
        return False
    keywords = ['local', 'function', 'game', 'if', 'then', 'return','print', 'wait']
    return any(keyword in source_code for keyword in keywords)

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        try:
            source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
        except:
            await ctx.reply("Error: Failed to read the attached file.")
            return
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    
    if not source_code or not source_code.strip():
        await ctx.reply("Please provide the txt / lua file")
        return

    if not is_valid_lua(source_code):
        await ctx.reply("Error: Script invalid.")
        return

    status_msg = await ctx.reply("Processing...")

    try:
        final_script = ironbrew_total_wrapped_v10_6(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        
        await ctx.send(
            content=f"{ctx.author.mention} Done.", 
            file=discord.File(file_stream, filename="message.txt")
        )
        await status_msg.delete()
    except Exception as e:
        await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    bot.run("TOKEN")
