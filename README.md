# dualsense-controller-python

Use the Dualsense Controller in Python

# Links / Inspiration

- [DualSense explorer tool](https://github.com/nondebug/dualsense)
- [pydualsense](https://github.com/flok/pydualsense)
- [ds5ctl](https://github.com/theY4Kman/ds5ctl)
- [USB_Host_Shield_2.0](https://github.com/felis/USB_Host_Shield_2.0)

# Protocol

## Sended data to controller

### Via USB

<table>
    <tr>
        <th>Byte Dec</th>
        <th>Byte Hex</th>
        <th>Name</th>
        <th>Values</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>0</td>
        <td>0x00</td>
        <td>Report ID</td>
        <td></td>
    </tr>
    <tr>
        <td>1</td>
        <td>0x01</td>
        <td>Feature flags (physical effects)</td>
        <td></td>
    </tr>
    <tr>
        <td>2</td>
        <td>0x02</td>
        <td>Feature flags (lights)</td>
        <td></td>
    </tr>
    <tr>
        <td>3</td>
        <td>0x03</td>
        <td>Motor rumble right</td>
        <td></td>
        <td>A.K.A. "small rumble"</td>
    </tr>
    <tr>
        <td>4</td>
        <td>0x04</td>
        <td>Motor rumble left</td>
        <td></td>
        <td>A.K.A. "big rumble"</td>
    </tr>
    <tr>
        <td>5</td>
        <td>0x05</td>
        <td></td>
        <td></td>
        <td>headphone, speaker, mic volume, audio flags (USB_Host_Shield_2.0)</td>
    </tr>
    <tr>
        <td>6</td>
        <td>0x06</td>
        <td></td>
        <td></td>
        <td>headphone, speaker, mic volume, audio flags (USB_Host_Shield_2.0)</td>
    </tr>
    <tr>
        <td>7</td>
        <td>0x07</td>
        <td></td>
        <td></td>
        <td>headphone, speaker, mic volume, audio flags (USB_Host_Shield_2.0)</td>
    </tr>
    <tr>
        <td>8</td>
        <td>0x08</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>9</td>
        <td>0x09</td>
        <td>Mute button led</td>
        <td>
            0x00 - Off <br>
            0x01 - On
        </td>
    </tr>
    <tr>
        <td>10</td>
        <td>0x0A</td>
        <td>Power save control</td>
        <td>
            0x00 - Unmute mic <br>
            0x10 - Mute mic
        </td>
    </tr>
    <tr>
        <td>11</td>
        <td>0x0B</td>
        <td>Right trigger - effect mode</td>
        <td>
            0x01 - CONTINUOUS_RESISTANCE <br> 
            0x02 - SECTION_RESISTANCE <br> 
            0x06 - VIBRATING <br> 
            0x23 - EFFECT_EXTENDED <br> 
            0xFC - CALIBRATE <br> 
        </td>
    </tr>
    <tr>
        <td>12</td>
        <td>0x0C</td>
        <td>Right trigger - Parameter 1</td>
        <td></td>
        <td>Start of resistance section</td>
    </tr>
    <tr>
        <td>13</td>
        <td>0x0D</td>
        <td>Right trigger - Parameter 2</td>
        <td></td>
    </tr>
    <tr>
        <td>14</td>
        <td>0x0E</td>
        <td>Right trigger - Parameter 3</td>
        <td></td>
    </tr>
    <tr>
        <td>15</td>
        <td>0x0F</td>
        <td>Right trigger - Parameter 4</td>
        <td></td>
    </tr>
    <tr>
        <td>16</td>
        <td>0x10</td>
        <td>Right trigger - Parameter 5</td>
        <td></td>
    </tr>
    <tr>
        <td>17</td>
        <td>0x11</td>
        <td>Right trigger - Parameter 6</td>
        <td></td>
    </tr>
    <tr>
        <td>18</td>
        <td>0x12</td>
        <td>Right trigger - Parameter 7</td>
        <td></td>
    </tr>
    <tr>
        <td>19</td>
        <td>0x13</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>20</td>
        <td>0x14</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>21</td>
        <td>0x15</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>22</td>
        <td>0x16</td>
        <td>Left trigger - effect mode</td>
        <td>
            0x01 - CONTINUOUS_RESISTANCE <br> 
            0x02 - SECTION_RESISTANCE <br> 
            0x06 - VIBRATING <br> 
            0x23 - EFFECT_EXTENDED <br> 
            0xFC - CALIBRATE <br> 
        </td>
    </tr>
    <tr>
        <td>23</td>
        <td>0x17</td>
        <td>Left trigger - Parameter 1</td>
        <td></td>
        <td>Start of resistance section</td>
    </tr>
    <tr>
        <td>24</td>
        <td>0x18</td>
        <td>Left trigger - Parameter 2</td>
        <td></td>
    </tr>
    <tr>
        <td>25</td>
        <td>0x19</td>
        <td>Left trigger - Parameter 3</td>
        <td></td>
    </tr>
    <tr>
        <td>26</td>
        <td>0x1A</td>
        <td>Left trigger - Parameter 4</td>
        <td></td>
    </tr>
    <tr>
        <td>27</td>
        <td>0x1B</td>
        <td>Left trigger - Parameter 5</td>
        <td></td>
    </tr>
    <tr>
        <td>28</td>
        <td>0x1C</td>
        <td>Left trigger - Parameter 6</td>
        <td></td>
    </tr>
    <tr>
        <td>29</td>
        <td>0x1D</td>
        <td>Left trigger - Parameter 7</td>
        <td></td>
    </tr>
    <tr>
        <td>30</td>
        <td>0x1E</td>
    </tr>
    <tr>
        <td>31</td>
        <td>0x1F</td>
    </tr>
    <tr>
        <td>32</td>
        <td>0x20</td>
    </tr>
    <tr>
        <td>33</td>
        <td>0x21</td>
    </tr>
    <tr>
        <td>34</td>
        <td>0x22</td>
    </tr>
    <tr>
        <td>35</td>
        <td>0x23</td>
    </tr>
    <tr>
        <td>36</td>
        <td>0x24</td>
    </tr>
    <tr>
        <td>37</td>
        <td>0x25</td>
        <td></td>
        <td></td>
        <td>Trigger motor effect strengths? (USB_Host_Shield_2.0)</td>
    </tr>
    <tr>
        <td>38</td>
        <td>0x26</td>
        <td></td>
        <td></td>
        <td>Speaker volume? (USB_Host_Shield_2.0)</td>
    </tr>
    <tr>
        <td>39</td>
        <td>0x27</td>
        <td></td>
        <td></td>
        <td>Led brightness, pulse? (USB_Host_Shield_2.0)</td>
    </tr>
    <tr>
        <td>40</td>
        <td>0x28</td>
        <td></td>
        <td></td>
        <td>LIGHTBAR_SETUP_CONTROL_ENABLE? (dualsense (Javascript))</td>
    </tr>
    <tr>
        <td>41</td>
        <td>0x29</td>
        <td>Lightbar control</td>
        <td>
            <nobr>
            0b100 - LIGHTBAR_CONTROL_ENABLE<br>
            0b000 - LIGHTBAR_CONTROL_DISABLE? 
            </nobr> 
        </td>
        <td></td>
    </tr>
    <tr>
        <td>42</td>
        <td>0x2A</td>
        <td>Lightbar setup</td>
        <td>
            <nobr>
            0x01 - LIGHT_ON <br>
            0x02 - LIGHT_OFF
            </nobr> 
        </td>
        <td></td>
    </tr>
    <tr>
        <td>43</td>
        <td>0x2B</td>
        <td>Led brightness</td>
        <td>
            <nobr>
            0x01 - FULL <br>
            0x02 - MEDIUM <br>
            0x03 - LOW
            </nobr> 
        </td>
        <td></td>
    </tr>
    <tr>
        <td>44</td>
        <td>0x2C</td>
        <td>Player leds</td>
        <td>
            <nobr>
                0b0000 - OFF <br>
                0b0100 - CENTER <br>
                0b1010 - INNER <br>
                0b1001 - OUTER <br>
                0b1111 - ALL
            </nobr> 
        </td>
        <td>
            CENTER: The single, center LED. <br>
            INNER: The two LEDs adjacent to and directly surrounding the CENTER LED. <br>
            OUTER: The two outermost LEDs surrounding the INNER LEDs.
        </td>
    </tr>
    <tr>
        <td>45</td>
        <td>0x2D</td>
        <td>Lightbar led color red</td>
        <td>
            0 - 255 
        </td>
        <td></td>
    </tr>
    <tr>
        <td>46</td>
        <td>0x2E</td>
        <td>Lightbar led color green</td>
        <td>
            0 - 255 
        </td>
        <td></td>
    </tr>
    <tr>
        <td>47</td>
        <td>0x2F</td>
        <td>Lightbar led color blue</td>
        <td>
            0 - 255 
        </td>
        <td></td>
    </tr>
</table>

