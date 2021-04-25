# class Program: #decl:List[Decl]

# class Decl(ABC): #abstract class

# class VarDecl(Decl): #name:str,typ:Type

# class ConstDecl(Decl): #name:str,val:Lit

# class FuncDecl(Decl): #name:str,param:List[VarDecl],body:Tuple(List[Decl],List[Expr])

# class Type(ABC): #abstract class

# class IntType(Type)

# class FloatType(Type)

# class Expr(ABC): #abstract class

# class Lit(Expr): #abstract class

# class IntLit(Lit): #val:int

# class Id(Expr): #name:str

# and exceptions:

# class RedeclaredVariable(Exception): #name:str

# class RedeclaredConstant(Exception): #name:str

# class RedeclaredFunction(Exception): #name:str

# class UndeclaredIdentifier(Exception): #name:str

# Implement the methods of the following class Visitor to travel on the above AST to detect undeclared declarations (throw the exception UndeclaredIdentifier). Note that the redeclared declarations exception also is thrown if a redeclared declaration is detected:

class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        o = []
        for x in ctx.decl:
            o.append(self.visit(x,o))

    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        return ctx.name
    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        return ctx.name
    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        sub_env = []
        for x in ctx.param:
            sub_env.append(self.visit(x,sub_env))
        for x in ctx.body[0]:
            if isinstance(x,FuncDecl):
                sub_env.append(self.visit(x,o+sub_env+[ctx.name]))
            else:
                sub_env.append(self.visit(x,sub_env))
        sub_env = o + sub_env+[ctx.name]
        for x in ctx.body[1]:
            self.visit(x,sub_env)
        return ctx.name
    def visitIntType(self,ctx:IntType,o:object):pass

    def visitFloatType(self,ctx:FloatType,o:object):pass

    def visitIntLit(self,ctx:IntLit,o:object):pass

    def visitId(self,ctx:Id,o:object):
        if not ctx.name in o:
            raise UndeclaredIdentifier(ctx.name)

# Program(
#     [
#         VarDecl("b",IntType()),
#         FuncDecl("a",[
#             VarDecl("m",FloatType()),
#             VarDecl("b",IntType()),
#             VarDecl("d",FloatType())],
#             (
#             [ConstDecl("c",IntLit(3)),
#             FuncDecl("foo",
#                 [VarDecl("x",IntType())],
#                 (
#                     [VarDecl("y",IntType()),VarDecl("z",IntType())],
#                     [Id("y"),Id("x"),Id("foo"),Id("c"),Id("m"),Id("a")])
#                 )],
#         [Id("foo"),Id("d"),Id("z")]
#             ))])