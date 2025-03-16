"""
スプライトアニメーションを管理するモジュール

スプライトシートからアニメーションを読み込み、管理します。
"""

import pygame
from typing import List, Dict, Optional
import os

class SpriteAnimation:
    """
    スプライトアニメーションを管理するクラス
    
    スプライトシートからフレームを切り出し、アニメーションを制御します。
    """
    
    def __init__(self, sprite_sheet_path: str, frame_width: int, frame_height: int,
                 frame_count: int, frame_duration: int = 5) -> None:
        """
        アニメーションを初期化します。
        
        Args:
            sprite_sheet_path (str): スプライトシートの画像パス
            frame_width (int): 1フレームの幅
            frame_height (int): 1フレームの高さ
            frame_count (int): フレーム数
            frame_duration (int): 1フレームの表示時間（フレーム数）
        """
        # スプライトシートの読み込み
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        # フレーム情報
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        
        # アニメーション制御用の変数
        self.current_frame = 0
        self.frame_timer = 0
        self.is_playing = True
        self.is_looping = True
        
        # フレームの切り出し
        self.frames = self._extract_frames()
        
        # 現在の画像
        self.image = self.frames[0]
        
        # 向き
        self.facing_right = True
    
    def _extract_frames(self) -> List[pygame.Surface]:
        """
        スプライトシートからフレームを切り出します。
        
        Returns:
            List[pygame.Surface]: 切り出したフレームのリスト
        """
        frames = []
        for i in range(self.frame_count):
            # フレームの切り出し位置を計算
            x = i * self.frame_width
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0),
                      (x, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames
    
    def update(self) -> None:
        """
        アニメーションを更新します。
        """
        if not self.is_playing:
            return
            
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame += 1
            
            if self.current_frame >= self.frame_count:
                if self.is_looping:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_count - 1
                    self.is_playing = False
            
            self.image = self.frames[self.current_frame]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
    
    def play(self, loop: bool = True) -> None:
        """
        アニメーションを再生します。
        
        Args:
            loop (bool): ループ再生するかどうか
        """
        self.is_playing = True
        self.is_looping = loop
        self.current_frame = 0
        self.frame_timer = 0
    
    def stop(self) -> None:
        """
        アニメーションを停止します。
        """
        self.is_playing = False
    
    def pause(self) -> None:
        """
        アニメーションを一時停止します。
        """
        self.is_playing = False
    
    def resume(self) -> None:
        """
        アニメーションを再開します。
        """
        self.is_playing = True
    
    def set_facing(self, facing_right: bool) -> None:
        """
        キャラクターの向きを設定します。
        
        Args:
            facing_right (bool): 右向きかどうか
        """
        if self.facing_right != facing_right:
            self.facing_right = facing_right
            self.image = pygame.transform.flip(self.image, True, False)
    
    def get_current_frame(self) -> pygame.Surface:
        """
        現在のフレームを取得します。
        
        Returns:
            pygame.Surface: 現在のフレームの画像
        """
        return self.image 