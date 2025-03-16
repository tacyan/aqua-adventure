"""
キャラクターのアニメーション状態を管理するモジュール

キャラクターの各状態（待機、移動、攻撃など）のアニメーションを管理します。
"""

import pygame
from typing import Dict, Optional
from .sprite_animation import SpriteAnimation
import os

class AnimationState:
    """
    アニメーション状態を表す列挙型のような定数クラス
    """
    IDLE = "idle"
    SWIM = "swim"
    ATTACK = "attack"
    HURT = "hurt"
    DASH = "dash"

class CharacterAnimation:
    """
    キャラクターのアニメーション状態を管理するクラス
    """
    
    def __init__(self, base_path: str) -> None:
        """
        キャラクターアニメーションを初期化します。
        
        Args:
            base_path (str): アニメーション画像の基本パス
        """
        self.animations: Dict[str, SpriteAnimation] = {}
        self.current_state = AnimationState.IDLE
        self.base_path = base_path
        
        # アニメーションの設定
        self._setup_animations()
    
    def _setup_animations(self) -> None:
        """
        各状態のアニメーションを設定します。
        """
        # 各状態のアニメーション設定
        animation_configs = {
            AnimationState.IDLE: {
                "file": "idle.png",
                "frame_width": 32,
                "frame_height": 32,
                "frame_count": 4,
                "frame_duration": 10
            },
            AnimationState.SWIM: {
                "file": "swim.png",
                "frame_width": 32,
                "frame_height": 32,
                "frame_count": 6,
                "frame_duration": 6
            },
            AnimationState.ATTACK: {
                "file": "attack.png",
                "frame_width": 32,
                "frame_height": 32,
                "frame_count": 4,
                "frame_duration": 5
            },
            AnimationState.HURT: {
                "file": "hurt.png",
                "frame_width": 32,
                "frame_height": 32,
                "frame_count": 2,
                "frame_duration": 5
            },
            AnimationState.DASH: {
                "file": "dash.png",
                "frame_width": 32,
                "frame_height": 32,
                "frame_count": 3,
                "frame_duration": 4
            }
        }
        
        # アニメーションの読み込み
        for state, config in animation_configs.items():
            file_path = os.path.join(self.base_path, config["file"])
            if os.path.exists(file_path):
                self.animations[state] = SpriteAnimation(
                    file_path,
                    config["frame_width"],
                    config["frame_height"],
                    config["frame_count"],
                    config["frame_duration"]
                )
    
    def update(self) -> None:
        """
        現在のアニメーション状態を更新します。
        """
        if self.current_state in self.animations:
            self.animations[self.current_state].update()
    
    def change_state(self, new_state: str) -> None:
        """
        アニメーション状態を変更します。
        
        Args:
            new_state (str): 新しい状態
        """
        if new_state in self.animations and new_state != self.current_state:
            self.current_state = new_state
            self.animations[new_state].play()
    
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        現在のフレームを取得します。
        
        Returns:
            Optional[pygame.Surface]: 現在のフレームの画像
        """
        if self.current_state in self.animations:
            return self.animations[self.current_state].get_current_frame()
        return None
    
    def set_facing(self, facing_right: bool) -> None:
        """
        キャラクターの向きを設定します。
        
        Args:
            facing_right (bool): 右向きかどうか
        """
        for animation in self.animations.values():
            animation.set_facing(facing_right) 