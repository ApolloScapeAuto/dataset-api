The table for indicating the record ids of forward driving and inverse driving on each road.
Blacked record ids are test sequences. 


|Road|Forward Time/Record ID|Inverse Time/Record ID| 
|---|---|---|
|road11|GZ20180310B/Record001-014, **GZ20180310B/Record015-20**|GZ20180310B/Record021-037, **GZ20180310B/Record037-046**|
|road12|CD20180303A/Record001-013, **CD20180303A/Record014-020**|CD20180303A/Record021-038, **CD20180303A/Record038-045**|
|road13|CD20180303G/Record001-014, **CD20180303G/Record018-024**|CD20180303G/Record025-049, **CD20180303G/Record050-064**|
|road14|BJ20180601B_A2/Record014-021, BJ20180601D_A2/Record016-021, **BJ20180602A_D2/Record001-006**|BJ20180601B_A2/Record001-007, BJ20180601D_A2/Record001-008, **BJ20180602A_D2/Record017-023**|
|road15|BJ20180602B_D2/Record020-027, **BJ20180602D_D2/Record001-006**|BJ20180602B_D2/Record001-007|
|road16|BJ20180603A_A2/Record001-007 BJ20180603E_D2/Record001-011 **BJ20180602I_D2/Record024-030**|BJ20180603A_A2/Record014-020 BJ20180603E_D2/Record021-026 **BJ20180602I_D2/Record001-008**|
|road17|BJ20180602G_D2/Record001-007  **BJ20180603B_A2/Record001-006**| BJ20180602G_D2/Record020-028|

In this table: we release the relative offset between different recording time stamp for each road, and testing time stamp are black bolded: 

|Road|Relative offset|
|---|---|
|road14|BJ20180601B_A2 -> BJ20180601D_A2: delta_X = 87, delta_Y = -98, delta_Z = 57; <br/> BJ20180601B_A2 -> **BJ20180602A_D2**: delta_X = -222, delta_Y = -371, delta_Z = 33;  |
|road15|BJ20180602B_D2 -> **BJ20180602D_D2**: delta_X = -30, delta_Y = -77, delta_Z = -5;|
|road16|BJ20180603A_A2 -> BJ20180603E_D2: delta_X = 247, delta_Y = 877, delta_Z = 25; <br/> BJ20180603A_A2 -> **BJ20180602I_D2**: delta_X = -822, delta_Y = 1089, delta_Z = -6;|
|road17|BJ20180602G_D2 -> **BJ20180603B_A2**: delta_X = 195, delta_Y = -339, delta_Z = 119;|
