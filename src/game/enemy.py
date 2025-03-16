"""
敵キャラクターの基本クラスを定義するモジュール

様々な敵キャラクターの基本となる機能を実装します。
"""

import pygame
from typing import Tuple, Optional
import math
import os
from .character_animation import CharacterAnimation, AnimationState

class Enemy(pygame.sprite.Sprite):
    """
    敵キャラクターの基本クラス
    
    すべての敵キャラクターの基本となる機能を提供します。
    """
    
    def __init__(self, x: float, y: float, hp: int = 10, enemy_type: str = "jellyfish") -> None:
        """
        敵キャラクターを初期化します。
        
        Args:
            x (float): 初期X座標
            y (float): 初期Y座標
            hp (int): 初期HP（デフォルト: 10）
            enemy_type (str): 敵の種類（デフォルト: "jellyfish"）
        """
        super().__init__()
        # アニメーションの初期化
        self.animation = CharacterAnimation(os.path.join("src", "assets", "images", "enemies", enemy_type))
        self.image = pygame.Surface((32, 32))  # デフォルト画像（アニメーションが読み込めない場合用）
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 物理演算用の変数
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        
        # ステータス
        self.maxHp = hp
        self.hp = hp
        self.damage = 10
        self.moveSpeed = 2.0
        
        # 状態フラグ
        self.isAlive = True
        self.facingRight = True
    
    def update(self, playerPos: pygame.math.Vector2) -> None:
        """
        敵の状態を更新します。
        
        Args:
            playerPos (pygame.math.Vector2): プレイヤーの現在位置
        """
        if not self.isAlive:
            return
            
        previous_state = self.animation.current_state
        self.moveTowardsPlayer(playerPos)
        
        # アニメーション状態の更新
        if not self.isAlive:
            self.animation.change_state(AnimationState.HURT)
        elif abs(self.velocity.x) > 0.1 or abs(self.velocity.y) > 0.1:
            self.animation.change_state(AnimationState.SWIM)
        else:
            self.animation.change_state(AnimationState.IDLE)
            
        # アニメーションの向きを設定
        self.animation.set_facing(self.facingRight)
        
        # アニメーションの更新
        self.animation.update()
        
        # 現在のフレームを取得して適用
        current_frame = self.animation.get_current_frame()
        if current_frame:
            self.image = current_frame
        
        # 位置の更新
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        # 画面外に出ないように制限
        self.constrainToScreen()
    
    def moveTowardsPlayer(self, playerPos: pygame.math.Vector2) -> None:
        """
        プレイヤーに向かって移動します。
        
        Args:
            playerPos (pygame.math.Vector2): プレイヤーの現在位置
        """
        direction = playerPos - self.position
        if direction.length() > 0:
            direction = direction.normalize()
            self.velocity = direction * self.moveSpeed
            
        # 向きの更新
        self.facingRight = direction.x > 0
    
    def constrainToScreen(self) -> None:
        """
        敵が画面外に出ないように位置を制限します。
        """
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x
        elif self.rect.right > 800:  # SCREEN_WIDTH
            self.rect.right = 800
            self.position.x = self.rect.x
            
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.y
        elif self.rect.bottom > 600:  # SCREEN_HEIGHT
            self.rect.bottom = 600
            self.position.y = self.rect.y
    
    def takeDamage(self, damage: int) -> None:
        """
        ダメージを受けた時の処理を行います。
        
        Args:
            damage (int): 受けるダメージ量
        """
        self.hp = max(0, self.hp - damage)
        self.animation.change_state(AnimationState.HURT)
        if self.hp <= 0:
            self.die()
    
    def die(self) -> None:
        """
        敵が倒された時の処理を行います。
        """
        self.isAlive = False
        # 死亡エフェクトやアイテムドロップなどの処理は後で実装
        
class Jellyfish(Enemy):
    """
    クラゲ型の敵クラス
    
    ゆっくりと上下に揺れながら移動する敵です。
    """
    
    def __init__(self, x: float, y: float) -> None:
        """
        クラゲを初期化します。
        
        Args:
            x (float): 初期X座標
            y (float): 初期Y座標
        """
        super().__init__(x, y, hp=5, enemy_type="jellyfish")
        self.moveSpeed = 1.5
        self.oscillationSpeed = 2.0
        self.oscillationAmplitude = 30
        self.initialY = y
        self.time = 0
    
    def update(self, playerPos: pygame.math.Vector2) -> None:
        """
        クラゲの状態を更新します。
        
        Args:
            playerPos (pygame.math.Vector2): プレイヤーの現在位置
        """
        if not self.isAlive:
            return
            
        # 横方向の移動
        direction = playerPos - self.position
        if direction.length() > 0:
            direction = direction.normalize()
            self.velocity.x = direction.x * self.moveSpeed
            
        # 上下の揺れ運動
        self.time += 0.016  # フレーム時間（1/60秒）
        self.position.y = self.initialY + math.sin(self.time * self.oscillationSpeed) * self.oscillationAmplitude
        self.position.x += self.velocity.x
        
        # 位置の更新
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        # 画面外に出ないように制限
        self.constrainToScreen() 