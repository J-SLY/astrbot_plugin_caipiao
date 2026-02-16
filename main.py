from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Node,Plain
@register("caipiao", "J-SLY", "一个虚拟货币系统", "1.0.0")
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
        user_id=event.get_sender_id()
        if await self.get_kv_data(f"is_{user_id}_rg", False) == False:
            await self.put_kv_data(f"{user_id}_money",1000)
            await self.put_kv_data(f"is_{user_id}_rg",True)
            yield event.plain_result("注册成功，初始资金：1000")
        else:
            yield event.plain_result(f"您({user_id})已经注册！")

    @vc.command("me",alias={'个人主页'})
    async def me(self,event:AstrMessageEvent):
        user_id=event.get_sender_id()
        is_rg = await self.get_kv_data(f"is_{user_id}_rg",False)
        if  is_rg == False:
            yield event.plain_result("您未注册！请使用/vc rg进行注册")
        else:
            person_info=Node(
                content=[
                    Plain(f"{user_id}的主页\n\n余额：{await self.get_kv_data(f'{user_id}_money',0)}")
                ]
            )
            yield event.chain_result([person_info])
    
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
