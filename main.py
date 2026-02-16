from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Node,Plain
from astrbot.api.event import AstrMessageEvent, filter, MessageChain
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
            await self.put_kv_data(f"{user_id}_money","1000")
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
    @filter.permission_type(filter.PermissionType.ADMIN)
    @vc.command("cg")
    async def cg(self,event:AstrMessageEvent,money:str,id:str,IsReal:bool=False):
        if IsReal==False:
            yield event.plain_result("请确认ID和金额后重新调用该指令")
        else:
            user_id=event.get_sender_id()
            if await self.get_kv_data(f"{user_id}_money",False)==False:
                yield event.plain_result(f"{user_id}用户不存在")
            else:
                last=await self.get_kv_data(f"{user_id}_money",False)
                await self.put_kv_data(f"{user_id}_money",money)
                yield event.plain_result(f"{user_id}的余额已由{last}改变为{money}")
    @vc.command("to",alias={'转账'})
    async def to(self,event:AstrMessageEvent,goal:str,money:int):
        user_id=event.get_sender_id
        to_id=goal
        if await self.get_kv_data(f"is_{user_id}_rg",False):
            yield event.plain_result(f"{user_id}未注册，请使用/vc rg注册")
        elif await self.get_kv_data(f"is_{to_id}_rg",False):
            yield event.plain_result(f"{to_id}未注册，请提醒对方使用/vc rg注册")
        else:
            user_money_str:str=str(await self.get_kv_data(f"{user_id}_money",0))
            user_money_int=int(user_money_str)
            to_money=int(money)
            if user_money_int<to_money:
                yield event.plain_result(f"你的账户剩余余额({user_money_str})不足，转账失败")
            else:
                goal_money_str=str(await self.get_kv_data(f"{goal}_money",0))
                goal_money_int=int(goal_money_str)
                await self.put_kv_data(f"{goal}_money",goal_money_int+money)
                await self.put_kv_data(f"{user_id}_money",user_money_int-money)
                yield event.plain_result(f"转账成功，您账户余额剩余{user_money_int-money}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
