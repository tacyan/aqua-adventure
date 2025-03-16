"""
泡の攻撃を実装するモジュール

プレイヤーが発射する泡の挙動を制御します。
"""

import pygame
from typing import Tuple

class Bubble(pygame.sprite.Sprite):
    """
    プレイヤーが発射する泡のクラス
    
    泡の移動、衝突判定、消滅などを管理します。
    """
    
    def __init__(self, x: float, y: float, direction: pygame.math.Vector2, power: int) -> None:
        """
        泡を初期化します。
        
        Args:
            x (float): 初期X座標
            y (float): 初期Y座標
            direction (pygame.math.Vector2): 発射方向
            power (int): 攻撃力
        """
        super().__init__()
        # 泡の画像を作成（後で実際の画像に置き換え）
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 200, 255, 128), (8, 8), 8)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # 物理演算用の変数
        self.position = pygame.math.Vector2(x, y)
        self.velocity = direction * 8.0  # 泡の速度
        
        # 泡のパラメータ
        self.power = power
        self.lifetime = 60  # 泡の寿命（フレーム数）
        self.isActive = True
    
    def update(self) -> bool:
        """
        泡の状態を更新します。
        
        Returns:
            bool: 泡がまだ有効かどうか
        """
        if not self.isActive:
            return False
            
        # 寿命の減少
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.isActive = False
            return False
            
        # 位置の更新
        self.position += self.velocity
        self.rect.center = self.position
        
        # 画面外に出たら消滅
        if (self.rect.right < 0 or self.rect.left > 800 or
            self.rect.bottom < 0 or self.rect.top > 600):
            self.isActive = False
            return False
            
        return True
    
    def hit(self) -> None:
        """
        泡が何かに当たった時の処理を行います。
        """
        self.isActive = False 