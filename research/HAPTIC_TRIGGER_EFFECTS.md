# Haptic Trigger Effects

## Trigger Bytes

<table>
    <tr>
        <th>BYTE</th>
        <th>FROM SOURCECODE</th>
        <th>PYDUALSENSE</th>
        <th>DSX</th>
    </tr>

<tr>    <td>0x00</td>   <td>NO_RESISTANCE        </td>  <td>Off        </td>    <td>CTV: OFF</td>  </tr>
<tr>    <td>0x01</td>   <td>CONTINUOUS_RESISTANCE</td>  <td>Rigid      </td>    <td>CTV: Rigid</td>    </tr>
<tr>    <td>0x02</td>   <td>SECTION_RESISTANCE   </td>  <td>Pulse      </td>    <td>CTV: Pulse, TM: GameTube Trigger</td>    </tr>
<tr>    <td>0x05</td>   <td>                     </td>  <td>Rigid_B    </td>    <td>CTV: Rigid B, TM: Normal Trigger, TM: Resistance (Force: 0)</td>  </tr>
<tr>    <td>0x21</td>   <td>                     </td>  <td>Rigid_A    </td>    <td>CTV: Rigid A</td>  </tr>
<tr>    <td>0x25</td>   <td>                     </td>  <td>Rigid_AB   </td>    <td>CTV: Rigid AB</td> </tr>
<tr>    <td>0x22</td>   <td>                     </td>  <td>Pulse_A    </td>    <td>CTV: Pulse A</td>  </tr>
<tr>    <td>0x26</td>   <td>EFFECT_EXTENDED      </td>  <td>Pulse_AB   </td>    <td>CTV: Pulse AB, CTV: VibrateResistance A, CTV: VibrateResistance AB</td>    </tr>
<tr>    <td>0x06</td>   <td>VIBRATING            </td>  <td>Pulse_B    </td>    <td>CTV: Pulse B, CTV: VibrateResistance, CTV: VibrateResistance B</td>    </tr>
<tr>    <td>0xFC</td>   <td>CALIBRATE            </td>  <td>Calibration</td>    <td></td>   </tr>
<tr>    <td>0x27</td>   <td>                     </td>  <td>           </td>    <td> CTV: Vibrate Pulse, CTV: Vibrate Pulse A, CTV: Vibrate Pulse B, CTV: Vibrate Pulse AB</td> </tr>
<tr>    <td>0x23</td>   <td>                     </td>  <td>           </td>    <td> TM: Bow </td> </tr>
</table>

## DSX Trigger Effect

### Normal Trigger

- CTV: Rigid B

```
                        M  1  2  3  4  5  6  7
                        
Normal Trigger          05 00 00 00 00 00 00 00
```

### GameTube Trigger

- CTV: Pulse

```
                        M  1  2  3  4  5  6  7
                        
GameTube Trigger        02 90 a0 ff 00 00 00 00     
```

### Bow - TODO

- Start: 0-8, End: 0-8, Force: 0-8, Snap Force: 0-8
- CTV: Pulse A

```
                        M  1  2  3  4  5  6  7
                        
Bow 1 8 8 1             22 02 01 07 00 00 00 00     
```

### Semi Automatic Gun

- Start: 2-7, End: 0-8, Force: 0-8
- CTV: Rigid AB
- CTV OFF, if End <= Start
- Normal Mode, if End > Start and Force < 1

```
                                                            M  1  2  3  4  5  6  7
Start                        
Semi Automatic Gun (Start: 2, End: 8, Force: 8)            25 04 01 07 00 00 00 00    
Semi Automatic Gun (Start: 3, End: 8, Force: 8)            25 08 01 07 00 00 00 00  
Semi Automatic Gun (Start: 4, End: 8, Force: 8)            25 10 01 07 00 00 00 00  
Semi Automatic Gun (Start: 5, End: 8, Force: 8)            25 20 01 07 00 00 00 00
Semi Automatic Gun (Start: 6, End: 8, Force: 8)            25 40 01 07 00 00 00 00
Semi Automatic Gun (Start: 7, End: 8, Force: 8)            25 80 01 07 00 00 00 00

End                       
Semi Automatic Gun (Start: 2, End: 2, Force: 8)            00 00 00 00 00 00 00 00
Semi Automatic Gun (Start: 2, End: 3, Force: 8)            25 0c 00 07 00 00 00 00
Semi Automatic Gun (Start: 2, End: 4, Force: 8)            25 14 00 07 00 00 00 00
Semi Automatic Gun (Start: 2, End: 5, Force: 8)            25 24 00 07 00 00 00 00
Semi Automatic Gun (Start: 2, End: 6, Force: 8)            25 44 00 07 00 00 00 00
Semi Automatic Gun (Start: 2, End: 7, Force: 8)            25 84 00 07 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 8)            25 04 01 07 00 00 00 00

Force                       
Semi Automatic Gun (Start: 2, End: 8, Force: 0)            05 00 00 00 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 1)            25 04 01 00 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 2)            25 04 01 01 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 3)            25 04 01 02 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 4)            25 04 01 03 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 5)            25 04 01 04 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 6)            25 04 01 05 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 7)            25 04 01 06 00 00 00 00
Semi Automatic Gun (Start: 2, End: 8, Force: 8)            25 04 01 07 00 00 00 00

Mixed
Semi Automatic Gun (Start: 2, End: 8, Force: 5)            25 04 01 04 00 00 00 00
Semi Automatic Gun (Start: 2, End: 6, Force: 5)            25 44 00 04 00 00 00 00
Semi Automatic Gun (Start: 2, End: 6, Force: 8)            25 44 00 07 00 00 00 00
Semi Automatic Gun (Start: 4, End: 8, Force: 5)            25 10 01 04 00 00 00 00
Semi Automatic Gun (Start: 4, End: 8, Force: 8)            25 10 01 07 00 00 00 00 
                                                           


```

### Automatic Gun

- Start: 0-9, Strength: 0-8, Frequency: 0-255
- CTV: Pulse AB
- Normal Trigger when strength or freq < 1

```
                                                        M  1  2  3  4  5  6  7
                                                        
Start
Automatic Gun (Start: 0, Strength: 8, Frequency: 9)     26 ff 03 ff ff ff 3f 09
Automatic Gun (Start: 1, Strength: 8, Frequency: 9)     26 fe 03 f8 ff ff 3f 09     
Automatic Gun (Start: 2, Strength: 8, Frequency: 9)     26 fc 03 c0 ff ff 3f 09     
Automatic Gun (Start: 3, Strength: 8, Frequency: 9)     26 f8 03 00 fe ff 3f 09    
Automatic Gun (Start: 4, Strength: 8, Frequency: 9)     26 f0 03 00 f0 ff 3f 09    
Automatic Gun (Start: 5, Strength: 8, Frequency: 9)     26 e0 03 00 80 ff 3f 09    
Automatic Gun (Start: 6, Strength: 8, Frequency: 9)     26 c0 03 00 00 fc 3f 09    
Automatic Gun (Start: 7, Strength: 8, Frequency: 9)     26 80 03 00 00 e0 3f 09    
Automatic Gun (Start: 8, Strength: 8, Frequency: 9)     26 00 03 00 00 00 3f 09    
Automatic Gun (Start: 9, Strength: 8, Frequency: 9)     26 00 02 00 00 00 38 09  

Strength
Automatic Gun (Start: 0, Strength: 0, Frequency: 9)     05 00 00 00 00 00 00 00
Automatic Gun (Start: 0, Strength: 1, Frequency: 9)     26 ff 03 00 00 00 00 09
Automatic Gun (Start: 0, Strength: 2, Frequency: 9)     26 ff 03 49 92 24 09 09
Automatic Gun (Start: 0, Strength: 3, Frequency: 9)     26 ff 03 92 24 49 12 09
Automatic Gun (Start: 0, Strength: 4, Frequency: 9)     26 ff 03 db b6 6d 1b 09
Automatic Gun (Start: 0, Strength: 5, Frequency: 9)     26 ff 03 24 49 92 24 09
Automatic Gun (Start: 0, Strength: 6, Frequency: 9)     26 ff 03 6d db b6 2d 09
Automatic Gun (Start: 0, Strength: 7, Frequency: 9)     26 ff 03 b6 6d db 36 09
Automatic Gun (Start: 0, Strength: 8, Frequency: 9)     26 ff 03 ff ff ff 3f 09

Freq
Automatic Gun (Start: 0, Strength: 8, Frequency: 0)     05 00 00 00 00 00 00 00
Automatic Gun (Start: 0, Strength: 8, Frequency: 1)     26 ff 03 ff ff ff 3f 01
Automatic Gun (Start: 0, Strength: 8, Frequency: 2)     26 ff 03 ff ff ff 3f 02
Automatic Gun (Start: 0, Strength: 8, Frequency: 3)     26 ff 03 ff ff ff 3f 03
Automatic Gun (Start: 0, Strength: 8, Frequency: 4)     26 ff 03 ff ff ff 3f 04
Automatic Gun (Start: 0, Strength: 8, Frequency: 5)     26 ff 03 ff ff ff 3f 05
Automatic Gun (Start: 0, Strength: 8, Frequency: 6)     26 ff 03 ff ff ff 3f 06
Automatic Gun (Start: 0, Strength: 8, Frequency: 7)     26 ff 03 ff ff ff 3f 07
Automatic Gun (Start: 0, Strength: 8, Frequency: 8)     26 ff 03 ff ff ff 3f 08
Automatic Gun (Start: 0, Strength: 8, Frequency: 9)     26 ff 03 ff ff ff 3f 09

  
```

### Galloping

- Byte: 0x23
- Start: 0-8, End: 0-9, First Foot: 0-6, Second Foot: 0-7, Frequency: 0-255

```
                                                                            M  1  2  3  4  5  6  7
                        
Galloping (Start: 0, End: 9, First Foot: 0, Second Foot: 7, Frequency: 3)   23 01 02 07 03 00 00 00 

Start, End 
Galloping (Start: 2, End: 7, First Foot: 0, Second Foot: 7, Frequency: 3)   23 84 00 07 03 00 00 00

First Foot, Second Foot
Galloping (Start: 0, End: 9, First Foot: 0, Second Foot: 5, Frequency: 3)   23 01 02 05 03 00 00 00

Frequency
Galloping (Start: 0, End: 9, First Foot: 0, Second Foot: 7, Frequency: 1)   23 01 02 07 01 00 00 00  (freq)
Galloping (Start: 0, End: 9, First Foot: 0, Second Foot: 7, Frequency: 4)   23 01 02 07 04 00 00 00  (freq)
Galloping (Start: 0, End: 9, First Foot: 0, Second Foot: 7, Frequency: 6)   23 01 02 07 06 00 00 00  (freq)

```

### Resistance

- CTV: Rigid B (Force: 0), CTV: Rigid_A
- Start: 0-9, Force: 0-8
- Normal Trigger if Force < 1
- Compared to Continous Resistance Mode (CTV: Rigid):
  - less strong
  - fewer steps

```
                                            M  1  2  3  4  5  6  7
                                            
Resistance (Start: 0-9, Force: 0)           05 00 00 00 00 00 00 00   

Force: Start: 0, Force 1-8  
Resistance (Start: 0, Force: 1)             21 ff 03 00 00 00 00 00     
Resistance (Start: 0, Force: 2)             21 ff 03 49 92 24 09 00 
Resistance (Start: 0, Force: 3)             21 ff 03 92 24 49 12 00 
Resistance (Start: 0, Force: 4)             21 ff 03 db b6 6d 1b 00 
Resistance (Start: 0, Force: 5)             21 ff 03 24 49 92 24 00 
Resistance (Start: 0, Force: 6)             21 ff 03 6d db b6 2d 00 
Resistance (Start: 0, Force: 7)             21 ff 03 b6 6d db 36 00 
Resistance (Start: 0, Force: 8)             21 ff 03 ff ff ff 3f 00 

Start: 0-9, Force: 1
Resistance (Start: 0, Force: 1)             21 ff 03 00 00 00 00 00 
Resistance (Start: 1, Force: 1)             21 fe 03 00 00 00 00 00 
Resistance (Start: 2, Force: 1)             21 fc 03 00 00 00 00 00 
Resistance (Start: 3, Force: 1)             21 f8 03 00 00 00 00 00  
Resistance (Start: 4, Force: 1)             21 f0 03 00 00 00 00 00  
Resistance (Start: 5, Force: 1)             21 e0 03 00 00 00 00 00   
Resistance (Start: 6, Force: 1)             21 c0 03 00 00 00 00 00   
Resistance (Start: 7, Force: 1)             21 80 03 00 00 00 00 00    
Resistance (Start: 8, Force: 1)             21 00 03 00 00 00 00 00     
Resistance (Start: 9, Force: 1)             21 00 02 00 00 00 00 00 

Start: 0-9, Force: 2  
Resistance (Start: 0, Force: 2)             21 ff 03 49 92 24 09 00
Resistance (Start: 1, Force: 2)             21 fe 03 48 92 24 09 00  
Resistance (Start: 2, Force: 2)             21 fc 03 40 92 24 09 00  
Resistance (Start: 3, Force: 2)             21 f8 03 00 92 24 09 00   
Resistance (Start: 4, Force: 2)             21 f0 03 00 90 24 09 00   
Resistance (Start: 5, Force: 2)             21 e0 03 00 80 24 09 00    
Resistance (Start: 6, Force: 2)             21 c0 03 00 00 24 09 00    
Resistance (Start: 7, Force: 2)             21 80 03 00 00 20 09 00     
Resistance (Start: 8, Force: 2)             21 00 03 00 00 00 09 00      
Resistance (Start: 9, Force: 2)             21 00 02 00 00 00 08 00  

Start: 0-9, Force: 3 
Resistance (Start: 0, Force: 3)             21 ff 03 92 24 49 12 00
Resistance (Start: 1, Force: 3)             21 fe 03 90 24 49 12 00  
Resistance (Start: 2, Force: 3)             21 fc 03 80 24 49 12 00  
Resistance (Start: 3, Force: 3)             21 f8 03 00 24 49 12 00  
Resistance (Start: 4, Force: 3)             21 f0 03 00 20 49 12 00   
Resistance (Start: 5, Force: 3)             21 e0 03 00 00 49 12 00    
Resistance (Start: 6, Force: 3)             21 c0 03 00 00 48 12 00    
Resistance (Start: 7, Force: 3)             21 80 03 00 00 40 12 00     
Resistance (Start: 8, Force: 3)             21 00 03 00 00 00 12 00      
Resistance (Start: 9, Force: 3)             21 00 02 00 00 00 10 00 

Start: 0-9, Force: 4
Resistance (Start: 0, Force: 4)             21 ff 03 db b6 6d 1b 00
Resistance (Start: 1, Force: 4)             21 fe 03 d8 b6 6d 1b 00  
Resistance (Start: 2, Force: 4)             21 fc 03 c0 b6 6d 1b 00  
Resistance (Start: 3, Force: 4)             21 f8 03 00 b6 6d 1b 00  
Resistance (Start: 4, Force: 4)             21 f0 03 00 b0 6d 1b 00  
Resistance (Start: 5, Force: 4)             21 e0 03 00 80 6d 1b 00    
Resistance (Start: 6, Force: 4)             21 c0 03 00 00 6c 1b 00    
Resistance (Start: 7, Force: 4)             21 80 03 00 00 60 1b 00     
Resistance (Start: 8, Force: 4)             21 00 03 00 00 00 1b 00      
Resistance (Start: 9, Force: 4)             21 00 02 00 00 00 18 00  

Start: 0-9, Force: 5   
Resistance (Start: 0, Force: 5)             21 ff 03 24 49 92 24 00
Resistance (Start: 1, Force: 5)             21 fe 03 20 49 92 24 00  
Resistance (Start: 2, Force: 5)             21 fc 03 00 49 92 24 00  
Resistance (Start: 3, Force: 5)             21 f8 03 00 48 92 24 00  
Resistance (Start: 4, Force: 5)             21 f0 03 00 40 92 24 00  
Resistance (Start: 5, Force: 5)             21 e0 03 00 00 92 24 00    
Resistance (Start: 6, Force: 5)             21 c0 03 00 00 90 24 00    
Resistance (Start: 7, Force: 5)             21 80 03 00 00 80 24 00     
Resistance (Start: 8, Force: 5)             21 00 03 00 00 00 24 00      
Resistance (Start: 9, Force: 5)             21 00 02 00 00 00 20 00   

Start: 0-9, Force: 6   
Resistance (Start: 0, Force: 6)             21 ff 03 6d db b6 2d 00
Resistance (Start: 1, Force: 6)             21 fe 03 68 db b6 2d 00  
Resistance (Start: 2, Force: 6)             21 fc 03 40 db b6 2d 00  
Resistance (Start: 3, Force: 6)             21 f8 03 00 da b6 2d 00  
Resistance (Start: 4, Force: 6)             21 f0 03 00 d0 b6 2d 00 
Resistance (Start: 5, Force: 6)             21 e0 03 00 80 b6 2d 00   
Resistance (Start: 6, Force: 6)             21 c0 03 00 00 b4 2d 00  
Resistance (Start: 7, Force: 6)             21 80 03 00 00 a0 2d 00   
Resistance (Start: 8, Force: 6)             21 00 03 00 00 00 2d 00  
Resistance (Start: 9, Force: 6)             21 00 02 00 00 00 28 00

Start: 0-9, Force: 7            
Resistance (Start: 0, Force: 7)             21 ff 03 b6 6d db 36 00  
Resistance (Start: 1, Force: 7)             21 fe 03 b0 6d db 36 00    
Resistance (Start: 2, Force: 7)             21 fc 03 80 6d db 36 00    
Resistance (Start: 3, Force: 7)             21 f8 03 00 6c db 36 00    
Resistance (Start: 4, Force: 7)             21 f0 03 00 60 db 36 00   
Resistance (Start: 5, Force: 7)             21 e0 03 00 00 db 36 00     
Resistance (Start: 6, Force: 7)             21 c0 03 00 00 d8 36 00    
Resistance (Start: 7, Force: 7)             21 80 03 00 00 c0 36 00     
Resistance (Start: 8, Force: 7)             21 00 03 00 00 00 36 00      
Resistance (Start: 9, Force: 7)             21 00 02 00 00 00 30 00
  
Start: 0-9, Force: 8           
Resistance (Start: 0, Force: 8)             21 ff 03 ff ff ff 3f 00  
Resistance (Start: 1, Force: 8)             21 fe 03 f8 ff ff 3f 00    
Resistance (Start: 2, Force: 8)             21 fc 03 c0 ff ff 3f 00    
Resistance (Start: 3, Force: 8)             21 f8 03 00 fe ff 3f 00    
Resistance (Start: 4, Force: 8)             21 f0 03 00 f0 ff 3f 00    
Resistance (Start: 5, Force: 8)             21 e0 03 00 80 ff 3f 00      
Resistance (Start: 6, Force: 8)             21 c0 03 00 00 fc 3f 00      
Resistance (Start: 7, Force: 8)             21 80 03 00 00 e0 3f 00        
Resistance (Start: 8, Force: 8)             21 00 03 00 00 00 3f 00        
Resistance (Start: 9, Force: 8)             21 00 02 00 00 00 38 00     
   
```

