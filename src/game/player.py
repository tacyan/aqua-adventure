"""
プレイヤーキャラクターの制御を行うモジュール

プレイヤーの移動、アクション、状態管理などを実装します。
"""

import pygame
from typing import Tuple, Optional, List
from .bubble import Bubble
from .character_animation import CharacterAnimation, AnimationState
import os

class Player(pygame.sprite.Sprite):
    """
    プレイヤーキャラクターを表すクラス
    
    プレイヤーの移動、アクション、状態などを管理します。
    """
    
    def __init__(self, x: float, y: float) -> None:
        """
        プレイヤーを初期化します。
        
        Args:
            x (float): 初期X座標
            y (float): 初期Y座標
        """
        super().__init__()
        # カービィの画像を読み込み
        try:
            self.original_image = pygame.image.load("img/Kirby.png")
            # 画像のサイズを48x48に調整
            self.original_image = pygame.transform.scale(self.original_image, (48, 48))
            self.image = self.original_image
        except pygame.error:
            # 画像が読み込めない場合は仮の画像を使用
            self.original_image = pygame.Surface((48, 48))
            self.original_image.fill((255, 192, 203))  # ピンク色（カービィっぽい色）
            self.image = self.original_image
            
        self.rect = self.image.get_rect()
        # 画面中央に配置するように位置を調整
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2
        
        # 物理演算用の変数
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        
        # ステータス
        self.maxHp = 100
        self.hp = self.maxHp
        self.maxStamina = 100
        self.stamina = self.maxStamina
        self.maxOxygen = 100
        self.oxygen = self.maxOxygen
        self.power = 10
        
        # 移動関連の定数
        self.MOVE_SPEED = 5.0
        self.DASH_SPEED = 8.0
        self.DASH_COST = 20  # ダッシュ時のスタミナ消費
        self.WATER_RESISTANCE = 0.9  # 水中の抵抗係数
        
        # 攻撃関連の定数
        self.BUBBLE_COOLDOWN = 20  # 泡の発射クールダウン（フレーム数）
        self.currentBubbleCooldown = 0
        
        # 状態フラグ
        self.isDashing = False
        self.isInvincible = False
        self.facingRight = True
        
        # 泡のリスト
        self.bubbles: List[Bubble] = []
    
    def handleInput(self) -> None:
        """
        キー入力を処理し、プレイヤーの移動とアクションを制御します。
        """
        keys = pygame.key.get_pressed()
        
        # 移動入力
        self.acceleration.x = 0
        self.acceleration.y = 0
        
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -self.MOVE_SPEED
            self.facingRight = False
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.MOVE_SPEED
            self.facingRight = True
        if keys[pygame.K_UP]:
            self.acceleration.y = -self.MOVE_SPEED
        if keys[pygame.K_DOWN]:
            self.acceleration.y = self.MOVE_SPEED
            
        # ダッシュ
        if keys[pygame.K_LSHIFT] and self.stamina >= self.DASH_COST:
            self.isDashing = True
            self.stamina -= self.DASH_COST * 0.016  # フレーム時間（1/60秒）で調整
        else:
            self.isDashing = False
            
        # 泡の発射（スペースキー）
        if keys[pygame.K_SPACE] and self.currentBubbleCooldown <= 0:
            self.shootBubble()
            self.currentBubbleCooldown = self.BUBBLE_COOLDOWN
    
    def update(self) -> None:
        """
        プレイヤーの状態を更新します。
        物理演算、ステータス更新などを行います。
        """
        self.handleInput()
        
        # 向きに応じて画像を反転
        if not self.facingRight:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image
        
        # クールダウンの更新
        if self.currentBubbleCooldown > 0:
            self.currentBubbleCooldown -= 1
        
        # 物理演算の更新
        if self.isDashing:
            self.velocity += self.acceleration * self.DASH_SPEED
        else:
            self.velocity += self.acceleration
            
        # 水中の抵抗を適用
        self.velocity *= self.WATER_RESISTANCE
        
        # 位置の更新
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        # 泡の更新
        self.updateBubbles()
        
        # ステータスの自然回復
        self.regenerateStatus()
        
        # 画面外に出ないように制限
        self.constrainToScreen()
    
    def updateBubbles(self) -> None:
        """
        発射された泡の状態を更新します。
        """
        # 無効になった泡を削除
        self.bubbles = [bubble for bubble in self.bubbles if bubble.update()]
    
    def regenerateStatus(self) -> None:
        """
        スタミナと酸素の自然回復処理を行います。
        """
        # スタミナの回復
        if not self.isDashing and self.stamina < self.maxStamina:
            self.stamina = min(self.maxStamina, self.stamina + 0.5)
            
        # 酸素の減少
        self.oxygen = max(0, self.oxygen - 0.1)
    
    def constrainToScreen(self) -> None:
        """
        プレイヤーが画面外に出ないように位置を制限します。
        """
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x
            self.velocity.x = 0
        elif self.rect.right > 800:  # SCREEN_WIDTH
            self.rect.right = 800
            self.position.x = self.rect.x
            self.velocity.x = 0
            
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.y
            self.velocity.y = 0
        elif self.rect.bottom > 600:  # SCREEN_HEIGHT
            self.rect.bottom = 600
            self.position.y = self.rect.y
            self.velocity.y = 0
    
    def shootBubble(self) -> None:
        """
        泡を発射します。
        """
        # 発射方向の決定
        direction = pygame.math.Vector2(1 if self.facingRight else -1, 0)
        
        # 泡の生成位置の調整（プレイヤーの中心から）
        bubbleX = self.rect.centerx + (20 if self.facingRight else -20)
        bubbleY = self.rect.centery
        
        # 泡の生成
        bubble = Bubble(bubbleX, bubbleY, direction, self.power)
        self.bubbles.append(bubble)
    
    def takeDamage(self, damage: int) -> None:
        """
        ダメージを受けた時の処理を行います。
        
        Args:
            damage (int): 受けるダメージ量
        """
        if not self.isInvincible:
            self.hp = max(0, self.hp - damage)
            self.isInvincible = True
            # 無敵時間の処理は後で実装
    
    def heal(self, amount: int) -> None:
        """
        HPを回復します。
        
        Args:
            amount (int): 回復量
        """
        self.hp = min(self.maxHp, self.hp + amount) 