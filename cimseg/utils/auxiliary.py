#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 17:50:54 2026

@author: roncofaber
"""

#%%

def number_to_well(n):
    """
    Convert number 0-15 to well position (A1, A2, ..., D4)
    
    Args:
        n: Integer from 0-15
    
    Returns:
        Well position string (e.g., 'A1', 'B3')
    """
    if not 0 <= n <= 15:
        raise ValueError("Number must be between 0 and 15")
    
    row = chr(65 + n // 4)  # 65 is ASCII for 'A'
    col = (n % 4) + 1
    
    return f"{row}{col}"