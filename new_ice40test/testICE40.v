`default_nettype none
module testICE40(input wire [19:0] PB,
                output wire [7:0] RIGHT,LEFT,
                output wire RED,GREEN,BLUE,
                output wire [7:0] SS0,SS1,SS2,
                SS3,SS4,SS5,SS6,SS7);
    assign RIGHT=PB[7:0];
    assign LEFT=PB[15:8];
    assign {RED,GREEN,BLUE}=PB[18:16];
    assign SS0=PB[7:0];
    assign SS1=PB[8:1];
    assign SS2=PB[9:2];
    assign SS3=PB[10:3];
    assign SS4=PB[16:9];
    assign SS5=PB[17:10];
    assign SS6=PB[18:11];
    assign SS7=PB[19:12];
endmodule
