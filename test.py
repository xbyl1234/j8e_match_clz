from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit


class Test(IScript):
    def run(self, ctx):
        sign = "LX/0aU;->A01(LX/0aU;LX/0Ig;)V"
        prj = ctx.getMainProject()
        dexUnit = prj.findUnit(IDexUnit)
        method = dexUnit.getMethod(sign)
        dexMethodData = method.getData()
        dexCodeItem = dexMethodData.getCodeItem()

        # 指令序列
        print("-------------------------------------")
        for idx, insn in enumerate(dexCodeItem.getInstructions()):
            print(idx, hex(insn.getOffset()), insn.getMnemonic())

        # 控制流图
        print("-------------------------------------")
        cfg = dexCodeItem.getControlFlowGraph()
        print(cfg)

        # 基本块信息
        print("-------------------------------------")
        blockList = cfg.getBlocks()
        for block in blockList:
            print("01 getFirstAddress           >>> ", hex(block.getFirstAddress()))  # 入口指令偏移
            print("02 getEndAddress             >>> ", hex(block.getEndAddress()))  # 出口指令偏移
            print("03 getLast                   >>> ", block.getLast())  # 最后一条指令
            print("04 getLastAddress            >>> ", hex(block.getLastAddress()))  # 最后一条指令偏移
            print("05 size                      >>> ", block.size())  # 指令条数
            print("06 getInstructions           >>> ", block.getInstructions())  # 指令序列
            print("07 allinsize                 >>> ", block.allinsize())  # 前驱个数
            print("08 insize                    >>> ", block.insize())  # 规则前驱个数
            print("09 irrinsize                 >>> ", block.irrinsize())  # 不规则前驱个数
            print("10 alloutsize                >>> ", block.alloutsize())  # 后继个数
            print("11 outsize                   >>> ", block.outsize())  # 规则后继个数
            print("12 irroutsize                >>> ", block.irroutsize())  # 不规则后继个数
            print("13 getAllInputBlocks         >>> ", block.getAllInputBlocks())  # 所有前驱块
            print("14 getInputBlocks            >>> ", block.getInputBlocks())  # 常规前驱块
            print("15 getIrregularInputBlocks   >>> ", block.getIrregularInputBlocks())  # 不规则前驱块
            print("16 getAllOutputBlocks        >>> ", block.getAllOutputBlocks())  # 所有后继块
            print("17 getOutputBlocks           >>> ", block.getOutputBlocks())  # 常规后继块
            print("18 getIrregularOutputBlocks  >>> ", block.getIrregularOutputBlocks())  # 不规则后继块
            print(block.getAddress())


