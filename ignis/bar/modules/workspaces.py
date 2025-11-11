#Ignis modules
from ignis import widgets
from ignis import utils
from ignis.services.niri import NiriService

#Generate service
niri = NiriService.get_default()

#Some consts
OPEN_WORKSPACE_SIZE=55
CONSTANT_Y_SIZE=11

class _WorkspaceItem(widgets.Overlay):

    

    def __init__(self, workspace_id: int):

        self.hovered=False;

        self.workspace_id = workspace_id

        self.middle_revealer = widgets.Revealer(
            child=widgets.Label(label="████"),
            reveal_child=False,
            transition_type="slide_right",
        )

        self.fixed_position_ball_child = widgets.FixedChild(
            widget=widgets.Label(
                label="🯩█🯫",
                style="font-family: BabelStone Pseudographica; font-size: 17px; color: red;",
            ),
            x=-2,
            y=CONSTANT_Y_SIZE
        )

        self.position_ball = widgets.Fixed(
            visible=False,
            child=[
                self.fixed_position_ball_child
            ]
        )

        super().__init__(
            child=widgets.EventBox(
                css_classes=["workspace_not_hover"],
                on_click=lambda self: self.get_parent()._change_current_workspace(),
                on_hover=lambda self: self.get_parent()._hover_enable(),
                on_hover_lost=lambda self: self.get_parent()._hover_disable(),
                style="font-family: BabelStone Pseudographica; font-size: 17px;",
                child=[
                    widgets.Label(label="🯩"),
                    self.middle_revealer,
                    widgets.Label(label="🯫")
                ]
            ),
            overlays=[
                self.position_ball,
            ]
        )
    
    def enable_disable(self):
        if self.middle_revealer.reveal_child:
            self.middle_revealer.reveal_child = False
            self.position_ball.visible = False
        else:
            self.middle_revealer.reveal_child = True
            self.position_ball.visible = True

    def _hover_enable(self):
        self.css_classes=["workspace_hover"]

    def _hover_disable(self):
        self.css_classes=["workspace_not_hover"]

    def _change_current_workspace(self):
        niri.switch_to_workspace(self.workspace_id)

    def reposition_bubble(self, new_window):
        if new_window.id == -1:
            self.position_ball.move(self.fixed_position_ball_child.widget,25,CONSTANT_Y_SIZE)
            return 0

        if new_window.layout.pos_in_scrolling_layout == None:
            return -1
        
        max_workspace_size=0
        for i in niri.windows:
            if i.workspace_id == self.workspace_id:
                max_workspace_size = max(max_workspace_size, i.layout.pos_in_scrolling_layout[0])

        if max_workspace_size == 1:
            self.position_ball.move(self.fixed_position_ball_child.widget,25,CONSTANT_Y_SIZE)
            return 0

        window_pos = new_window.layout.pos_in_scrolling_layout[0]
        window_pos = int((window_pos-1)/(max_workspace_size-1)*OPEN_WORKSPACE_SIZE-2)

        self.position_ball.move(self.fixed_position_ball_child.widget,window_pos,CONSTANT_Y_SIZE)
        

class Workspaces(widgets.Box):

    def __init__(self):
        self.current_workspace: _WorkspaceItem = None
        
        super().__init__();

        workspace_amount=len(niri.workspaces)
        for i in range(workspace_amount):
            self.append(_WorkspaceItem(i+1))

        niri.connect("notify::workspaces", self.update_workspace_count)
        
        for i in niri.workspaces:
            if i.is_active:
                self.current_workspace = self.child[i.idx-1]
                self.current_workspace.enable_disable()

        niri.active_window.connect("notify::id", self._reposition_active_bubble)
        

    def update_workspace_count(self, *_):
        niri_workspaces = len(niri.workspaces)
        child_instance = len(self.child)
    
        if niri_workspaces < child_instance:
            self._remove_workspace()
        elif niri_workspaces == child_instance:
            self._reposition_workspace()
            self._reposition_active_bubble(niri.active_window)
        else:
            self._add_workspace()

    def _add_workspace(self):
        self.append(_WorkspaceItem(len(self.child)+1))

    def _remove_workspace(self):
        self.remove(self.child[-1])

    def _reposition_workspace(self):
        for i in niri.workspaces:
            if i.is_active:
                self.current_workspace.enable_disable()
                self.current_workspace = self.child[i.idx-1]
                self.current_workspace.enable_disable()

    def _reposition_active_bubble(self, new_window, *_):
        self.current_workspace.reposition_bubble(new_window)

#Aviam, aqui hem de ficar:
#-Funcions per quan es crea i desapareixen workspaces
#-Funcions per canviar i actualitzar centered workspace
#-Funció amb signal per qun canvii la posició actual del workspace
#Utilitzant els símbols de computació antiga i BabelStone PSeudographica, podem
#aconseguri tenir algo similar a una elipsis. Si fiquem amb zero hspace:
#- Una label amb el primer semicercle
#- Una label amb el segons semicercle
#- Un revealer amb la quantitat de full size boxes que calgui
#I activem el revealer quan està actiu, si de veritat hi ha zero hspace, s'hauria
#de veure com s'obre i es tanca amb poca dificultat, però hem d'aconseguir aquest
#zero hspace.
#Llavors, amb un overlay, podem dibuixar un altre cercle que mostri on ets del workspace
#bof que xulo quedarà

