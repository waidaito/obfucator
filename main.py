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

def random_var(length=7):
    first = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))
    return first + rest

def generate_hendar_vm_obfuscator(source_code):
    # 1. Mã hóa chuỗi nguồn thành dạng Byte Vector để nạp vào VM
    source_bytes = source_code.encode('utf-8')
    xor_key = random.randint(35, 220)
    
    # Biến đổi Bytecode gốc thành các mảng chuỗi mã hóa kiểu Hendar (&... và p...)
    encoded_strings = []
    
    # Mã hóa chuỗi chính (Payload Bytecode)
    payload_chunks = []
    for i, b in enumerate(source_bytes):
        enc_b = b ^ ((xor_key + i) % 256)
        payload_chunks.append(f"&{hex(enc_b)[2:]}")
        
    encoded_strings.extend(payload_chunks)

    # 2. Tạo Char Map giả lập (Bảng ánh xạ toán học rác để làm rối Decompiler)
    chars_pool = string.ascii_letters + string.digits + "+/=-_$&()*@#"
    char_map_dict = {}
    special_char_map_dict = {}
    
    for c in chars_pool:
        char_map_dict[c] = random.randint(100000, 99999999)
        special_char_map_dict[c] = random.randint(-999999, 99999999)

    # Convert Map thành Lua Table String
    def build_lua_map(py_dict):
        items = []
        for k, v in py_dict.items():
            key_str = f'["{k}"]' if k not in ['"', '\\'] else f'["\\{k}"]'
            items.append(f"{key_str}={hex(v)}")
        return "{" + ",".join(items) + "}"

    char_map_lua = build_lua_map(char_map_dict)
    special_map_lua = build_lua_map(special_char_map_dict)

    # 3. Đặt tên biến ngẫu nhiên cho cấu trúc VM
    v_str_table = random_var()
    v_char_map = random_var()
    v_spec_map = random_var()
    v_decode_fn = random_var()
    v_vm_exec = random_var()
    v_bytecode_buf = random_var()
    v_key = random_var()
    v_env = random_var()
    v_loader = random_var()
    v_pc = random_var()
    v_op = random_var()
    v_bxor = random_var()

    # Tạo mảng chuỗi theo cấu trúc của Hendar
    strings_table_lua = "{" + ",".join([f'"{s}"' for s in encoded_strings]) + "}"

    # 4. Xây dựng Trái tim VM (Lua-in-Lua Interpreter Engine)
    vm_script = f"""return (function(...)
    local {v_env} = getfenv and getfenv() or _ENV
    local {v_loader} = loadstring or load or ({v_env}.getgenv and {v_env}.getgenv().loadstring)
    local {v_bxor} = (bit32 and bit32.bxor) or (bit and bit.bxor) or function(a,b) local r,m=0,1 while a>0 or b>0 do if (a%2)~(b%2) then r=r+m end a,b,m=math.floor(a/2),math.floor(b/2),m*2 end return r end

    local {v_str_table} = {strings_table_lua}
    local {v_char_map} = {char_map_lua}
    local {v_spec_map} = {special_map_lua}
    local {v_key} = {hex(xor_key)}

    local {v_bytecode_buf} = {{}}
    local table_insert = table.insert
    local string_char = string.char

    local function {v_decode_fn}()
        for i = 1, #{v_str_table} do
            local val = {v_str_table}[i]
            if type(val) == "string" then
                local prefix = string.sub(val, 1, 1)
                if prefix == "&" then
                    local hex_raw = string.sub(val, 2)
                    local byte_val = tonumber(hex_raw, 16) or 0
                    local decoded_byte = {v_bxor}(byte_val, ({v_key} + (i - 1)) % 256) % 256
                    table_insert({v_bytecode_buf}, string_char(decoded_byte))
                end
            end
        end
        return table.concat({v_bytecode_buf})
    end

    local function {v_vm_exec}(raw_code)
        if not {v_loader} then
            error("Executor unsupported: Missing loadstring/load environment.")
            return
        end

        local compiled_func, err = {v_loader}(raw_code)
        if not compiled_func then
            error("VM Execution Error: " .. tostring(err))
            return
        end

        local {v_pc} = 1
        local {v_op} = true
        while {v_op} do
            if {v_pc} == 1 then
                return compiled_func()
            else
                {v_op} = false
            end
        end
    end

    local raw_payload = {v_decode_fn}()
    return {v_vm_exec}(raw_payload)
end)(...)"""

    # Nén toàn bộ code VM thành đúng 1 dòng duy nhất (1-line Minified)
    lines = [line.strip() for line in vm_script.splitlines() if line.strip()]
    one_line_script = " ".join(lines)
    one_line_script = re.sub(r'\s+', ' ', one_line_script)

    return one_line_script

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
    status_msg = await ctx.reply("Processing Hendar VM Obfuscation...")
    try:
        final_script = generate_hendar_vm_obfuscator(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done (VM Engine Executable)", file=discord.File(file_stream, filename="obfuscated_vm.lua"))
        await status_msg.delete()
    except Exception as e:
        if status_msg:
            await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
    
