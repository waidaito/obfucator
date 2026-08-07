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

# [ GIỮ NGUYÊN HÀM TẠO RÁC CỦA ÔNG ]
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

# [ LÕI COMPILER CHO VM (KHÔNG DÙNG LOADSTRING) ]
class TrueLuaVMCompiler:
    def __init__(self, source_code):
        self.source = source_code
        self.constants = []
        self.const_map = {}
        self.instructions = []
        
        op_list = list(range(1, 15))
        random.shuffle(op_list)
        self.OP_GETGLOBAL, self.OP_LOADK, self.OP_MOVE, self.OP_GETTABLE = op_list[0:4]
        self.OP_SETTABLE, self.OP_SETGLOBAL, self.OP_CALL, self.OP_METHOD = op_list[4:8]
        self.OP_NEWTABLE, self.OP_RETURN = op_list[8:10]

    def add_const(self, val):
        if val not in self.const_map:
            self.constants.append(val)
            self.const_map[val] = len(self.constants)
        return self.const_map[val]

    def compile(self):
        clean_code = re.sub(r'--.*', '', self.source)
        statements = [s.strip() for s in clean_code.split(';') if s.strip()]
        if not statements:
            statements = [line.strip() for line in clean_code.splitlines() if line.strip()]

        for stmt in statements:
            self.compile_statement(stmt)
        self.instructions.append([self.OP_RETURN, 0, 0, 0])
        return self.constants, self.instructions

    def compile_statement(self, stmt):
        method_match = re.match(r'^([a-zA-Z0-9_\.\:]+)\s*\((.*)\)$', stmt)
        if method_match:
            func_expr, args_str = method_match.groups()
            self.compile_call(func_expr, args_str)
            return

        assign_match = re.match(r'^(?:local\s+)?([a-zA-Z0-9_\.]+)\s*=\s*(.+)$', stmt)
        if assign_match:
            var_name, val_expr = assign_match.groups()
            self.compile_assignment(var_name, val_expr)
            return
        self.add_const(stmt)

    def compile_call(self, func_expr, args_str):
        args = []
        if args_str.strip():
            raw_args = [a.strip() for a in args_str.split(',')]
            for arg in raw_args:
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    args.append(('string', arg[1:-1]))
                elif arg.isdigit():
                    args.append(('number', int(arg)))
                elif arg in ['true', 'false']:
                    args.append(('bool', arg == 'true'))
                else:
                    args.append(('var', arg))

        if ':' in func_expr:
            obj_name, method_name = func_expr.split(':', 1)
            c_obj = self.add_const(obj_name)
            self.instructions.append([self.OP_GETGLOBAL, 1, c_obj, 0])
            c_method = self.add_const(method_name)
            self.instructions.append([self.OP_METHOD, 2, 1, c_method])
            
            for idx, (atype, aval) in enumerate(args):
                r = 4 + idx
                c_idx = self.add_const(aval)
                if atype in ['string', 'number', 'bool']:
                    self.instructions.append([self.OP_LOADK, r, c_idx, 0])
                else:
                    self.instructions.append([self.OP_GETGLOBAL, r, c_idx, 0])
            self.instructions.append([self.OP_CALL, 2, len(args) + 1, 0])
        else:
            c_fn = self.add_const(func_expr)
            self.instructions.append([self.OP_GETGLOBAL, 1, c_fn, 0])
            for idx, (atype, aval) in enumerate(args):
                r = 2 + idx
                c_idx = self.add_const(aval)
                if atype in ['string', 'number', 'bool']:
                    self.instructions.append([self.OP_LOADK, r, c_idx, 0])
                else:
                    self.instructions.append([self.OP_GETGLOBAL, r, c_idx, 0])
            self.instructions.append([self.OP_CALL, 1, len(args), 0])

    def compile_assignment(self, var_name, val_expr):
        c_var = self.add_const(var_name)
        if (val_expr.startswith('"') and val_expr.endswith('"')) or (val_expr.startswith("'") and val_expr.endswith("'")):
            c_val = self.add_const(val_expr[1:-1])
            self.instructions.append([self.OP_LOADK, 1, c_val, 0])
        elif val_expr.isdigit():
            c_val = self.add_const(int(val_expr))
            self.instructions.append([self.OP_LOADK, 1, c_val, 0])
        else:
            c_val = self.add_const(val_expr)
            self.instructions.append([self.OP_GETGLOBAL, 1, c_val, 0])
        self.instructions.append([self.OP_SETGLOBAL, c_var, 1, 0])

# [ HỆ THỐNG GHÉP VM + RÁC VÀ ĐẢO KEY CỦA ÔNG ]
def true_vm_integrated_engine(source_code):
    compiler = TrueLuaVMCompiler(source_code)
    constants, instructions = compiler.compile()

    # Thuật toán sinh Multi-Key của ông
    keys_count = random.randint(7, 12)
    keys_list = [random.randint(50, 255) for _ in range(keys_count)]
    
    # Mã hóa hằng số (Constants) của VM dựa trên Multi-Key Array
    enc_constants = []
    for const in constants:
        const_str = str(const).encode('utf-8')
        current_keys = list(keys_list)
        hex_list = []
        for idx, byte in enumerate(const_str):
            cipher_byte = byte
            for k in current_keys:
                cipher_byte ^= k
            hex_list.append(f"{cipher_byte:02X}")
            for k_idx in range(len(current_keys)):
                current_keys[k_idx] = (current_keys[k_idx] + idx + (k_idx + 3)) % 256
        enc_constants.append(f'"{ "".join(hex_list) }"')

    # Sinh 11.000 dòng rác
    junk_pieces = []
    for _ in range(11000):
        v_junk = random_var()
        rand_target = random.randint(50, 99999)
        junk_pieces.append(f"local {v_junk}={generate_clean_advanced_junk(rand_target)}")
    half = len(junk_pieces) // 2
    junk_top = ";".join(junk_pieces[:half])
    junk_bottom = ";".join(junk_pieces[half:])
    
    # Mã hóa mảng Key bằng thuật toán rác
    matrix_elements = []
    for k_idx, k_val in enumerate(keys_list):
        matrix_elements.append(f"{{{obfuscate_core_math(k_val)},{obfuscate_core_math(k_idx + 3)}}}")
    matrix_elements.reverse()
    matrix_str = ",".join(matrix_elements)

    enc_instructions = []
    for inst in instructions:
        enc_instructions.append("{" + ",".join(map(str, inst)) + "}")

    # Random Tên Biến VM
    v_env, v_consts, v_insts, v_regs, v_pc, v_bxor, v_decode_c = [random_var() for _ in range(7)]

    # Dựng Engine Máy Ảo bằng Lua
    vm_core = f"""
    local {v_env} = getfenv and getfenv() or _ENV;
    local {v_bxor} = (bit32 and bit32.bxor) or (bit and bit.bxor) or function(a,b) local r,m=0,1 while a>0 or b>0 do if (a%2)~(b%2) then r=r+m end a,b,m=math.floor(a/2),math.floor(b/2),m*2 end return r end;

    local raw_consts = {{{ ",".join(enc_constants) }}};
    local {v_consts} = {{}};

    local function {v_decode_c}(hex_str)
        local matrix = {{{matrix_str}}};
        local res = {{}};
        local byte_idx = 0;
        for i = 1, #hex_str, 2 do
            local num = tonumber(string.sub(hex_str, i, i+1), 16) or 0;
            local dec = num;
            for k = 1, #matrix do
                dec = {v_bxor}(dec, matrix[k][1]);
            end;
            table.insert(res, string.char(dec));
            for k = 1, #matrix do
                matrix[k][1] = (matrix[k][1] + byte_idx + matrix[k][2]) % 256;
            end;
            byte_idx = byte_idx + 1;
        end;
        local s = table.concat(res);
        if tonumber(s) then return tonumber(s) end;
        if s=="true" then return true end;
        if s=="false" then return false end;
        return s;
    end;

    for i = 1, #raw_consts do
        {v_consts}[i] = {v_decode_c}(raw_consts[i]);
    end;

    local {v_insts} = {{{ ",".join(enc_instructions) }}};
    local {v_regs} = {{}};
    local {v_pc} = 1;

    while {v_pc} <= #{v_insts} do
        local inst = {v_insts}[{v_pc}];
        local op = inst[1];

        if op == {compiler.OP_GETGLOBAL} then
            {v_regs}[inst[2]] = {v_env}[{v_consts}[inst[3]]];
        elseif op == {compiler.OP_LOADK} then
            {v_regs}[inst[2]] = {v_consts}[inst[3]];
        elseif op == {compiler.OP_MOVE} then
            {v_regs}[inst[2]] = {v_regs}[inst[3]];
        elseif op == {compiler.OP_GETTABLE} then
            {v_regs}[inst[2]] = {v_regs}[inst[3]][{v_consts}[inst[4]]];
        elseif op == {compiler.OP_SETTABLE} then
            {v_regs}[inst[2]][{v_consts}[inst[3]]] = {v_regs}[inst[4]];
        elseif op == {compiler.OP_SETGLOBAL} then
            {v_env}[{v_consts}[inst[2]]] = {v_regs}[inst[3]];
        elseif op == {compiler.OP_METHOD} then
            local obj = {v_regs}[inst[3]];
            {v_regs}[inst[2]] = obj[{v_consts}[inst[4]]];
            {v_regs}[inst[2] + 1] = obj;
        elseif op == {compiler.OP_CALL} then
            local fn = {v_regs}[inst[2]];
            local arg_cnt = inst[3];
            local args = {{}};
            for i = 1, arg_cnt do
                table.insert(args, {v_regs}[inst[2] + i]);
            end;
            local res = {{fn(unpack(args))}};
            {v_regs}[inst[2]] = res[1];
        elseif op == {compiler.OP_NEWTABLE} then
            {v_regs}[inst[2]] = {{}};
        elseif op == {compiler.OP_RETURN} then
            return;
        end;

        {v_pc} = {v_pc} + 1;
    end;
    """

    # Gộp tất cả: Rác trên + VM Engine + Rác dưới
    total_payload = f"{junk_top};{vm_core};{junk_bottom}"
    clean_payload = " ".join(total_payload.splitlines()).strip().replace(" ; ", ";").replace(";;", ";")
    
    return f"-- True VM Enigme by Hendar (No Loadstring) --\nreturn (function(...) {clean_payload} end)(...)"

@bot.command(name="obf")
async def obf_command(ctx, *, text_code: str = None):
    source_code = None
    if ctx.message.attachments:
        source_code = (await ctx.message.attachments[0].read()).decode(errors="ignore")
    elif text_code:
        source_code = re.sub(r'^```[a-zA-Z]*\n|```$', '', text_code.strip(), flags=re.MULTILINE)
    
    if not source_code or not source_code.strip():
        return await ctx.reply("Please add file / code.")
    
    status_msg = await ctx.reply("Processing True VM with Heavy Junk...")
    try:
        final_script = true_vm_integrated_engine(source_code)
        file_stream = io.BytesIO(final_script.encode('utf-8'))
        await ctx.send(content=f"{ctx.author.mention} Done (True VM - Anti Loadstring Hook)", file=discord.File(file_stream, filename="obfuscated_vm.lua"))
        await status_msg.delete()
    except Exception as e:
        if status_msg:
            await status_msg.delete()
        await ctx.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.run(os.getenv("TOKEN"))
        
