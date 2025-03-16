"""
ゲームの状態管理とシーン遷移を実装するモジュール

ゲームの各状態（タイトル、プレイ中、ポーズなど）の管理と
シーン間の遷移を制御します。
"""

from enum import Enum, auto
from typing import Dict, Optional, Callable
import pygame

class GameState(Enum):
    """
    ゲームの状態を表す列挙型
    """
    TITLE = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

class SceneManager:
    """
    ゲームのシーン管理を行うクラス
    
    各シーンの更新と描画、シーン間の遷移を管理します。
    """
    
    def __init__(self) -> None:
        """
        シーンマネージャーを初期化します。
        """
        self.currentState = GameState.TITLE
        self.nextState: Optional[GameState] = None
        self.isTransitioning = False
        self.transitionAlpha = 0
        self.TRANSITION_SPEED = 5
        
        # トランジション用のサーフェス
        self.transitionSurface = pygame.Surface((800, 600))  # SCREEN_WIDTH, SCREEN_HEIGHT
        self.transitionSurface.fill((0, 0, 0))
        
        # 状態ごとの更新処理と描画処理を登録
        self.updateHandlers: Dict[GameState, Callable[[], None]] = {}
        self.renderHandlers: Dict[GameState, Callable[[pygame.Surface], None]] = {}
    
    def registerHandlers(self, state: GameState,
                        updateHandler: Callable[[], None],
                        renderHandler: Callable[[pygame.Surface], None]) -> None:
        """
        状態ごとの処理ハンドラを登録します。
        
        Args:
            state (GameState): ゲームの状態
            updateHandler (Callable[[], None]): 更新処理を行う関数
            renderHandler (Callable[[pygame.Surface], None]): 描画処理を行う関数
        """
        self.updateHandlers[state] = updateHandler
        self.renderHandlers[state] = renderHandler
    
    def changeState(self, newState: GameState) -> None:
        """
        ゲームの状態を変更します。
        
        Args:
            newState (GameState): 新しい状態
        """
        if not self.isTransitioning:
            self.nextState = newState
            self.isTransitioning = True
    
    def update(self) -> None:
        """
        現在の状態の更新処理を実行します。
        """
        if self.isTransitioning:
            self.updateTransition()
        else:
            if self.currentState in self.updateHandlers:
                self.updateHandlers[self.currentState]()
    
    def render(self, screen: pygame.Surface) -> None:
        """
        現在の状態の描画処理を実行します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        if self.currentState in self.renderHandlers:
            self.renderHandlers[self.currentState](screen)
            
        if self.isTransitioning:
            self.renderTransition(screen)
    
    def updateTransition(self) -> None:
        """
        シーン遷移のアニメーションを更新します。
        """
        if self.nextState is None:
            return
            
        if self.transitionAlpha < 255:
            # フェードアウト
            self.transitionAlpha = min(255, self.transitionAlpha + self.TRANSITION_SPEED)
        else:
            # 状態の切り替えとフェードイン
            self.currentState = self.nextState
            self.transitionAlpha = max(0, self.transitionAlpha - self.TRANSITION_SPEED)
            if self.transitionAlpha == 0:
                self.isTransitioning = False
                self.nextState = None
    
    def renderTransition(self, screen: pygame.Surface) -> None:
        """
        シーン遷移のアニメーションを描画します。
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        self.transitionSurface.set_alpha(self.transitionAlpha)
        screen.blit(self.transitionSurface, (0, 0))
    
    def getCurrentState(self) -> GameState:
        """
        現在のゲーム状態を取得します。
        
        Returns:
            GameState: 現在のゲーム状態
        """
        return self.currentState 