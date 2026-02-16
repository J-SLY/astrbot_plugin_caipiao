from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Node,Plain   

@register("caipiao", "J-SLY", "一个虚拟货币系统", "1.0.0")
class user:
    id:str
    menoy:int
    today_is_buy_cp:bool
    today_cp_num:list=[[],[]]
    def __init__(self,id:str):
        self.id=id
        self.menoy=1000
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command_group("vc")
    def vc(self):
        pass
    @vc.command("help",alias={'帮助'})
    async def help(self, event: AstrMessageEvent):
        help_text=Node(
            content=[
                Plain("帮助文档：\n\n /vc help /vc 帮助 ：输出本帮助列表\n")
            ]
        )
        yield event.chain_result([help_text])
    @vc.command("rg",alias={'注册'})
    async def rg(self,event:AstrMessageEvent):
        if await self.get_kv_data(f"{event.get_sender_id()}", False) == False:
            tmp_user:user=user(event.get_sender_id())
            await self.put_kv_data(f"{event.get_sender_id()}",tmp_user) # type: ignore
            yield event.plain_result("注册成功，初始资金：1000")
        else:
            yield event.plain_result(f"您{event.get_sender_id()}已经注册！")

    @vc.command("me",alias={'个人主页'})
    async def me(self,event:AstrMessageEvent):
        person = await self.get_kv_data(f"{event.get_sender_id()}",False)
        if  person== False:
            yield event.plain_result("您未注册！请使用/vc rg进行注册")
        else:
            person_info=Node(
                content=[
                    Plain(f"{event.get_sender_id}的个人主页\n\nID：{event.get_sender_id()}\n余额：{event.get_sender_id()}")
                ]
            )
            yield event.chain_result([person_info])
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
