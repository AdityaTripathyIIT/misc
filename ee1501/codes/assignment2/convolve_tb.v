`timescale 1ns/1ps
module convolution_tb;
    reg [3:0] x[0:7];
    reg [3:0] h[0:7];
    wire [3:0] y[0:14];
    
    convolution dut (
        .x(x),
        .h(h),
        .y(y)
    );

    initial begin
        $dumpfile("wave1.vcd");
        $dumpvars(0, convolution_tb);

        // Dump individual array elements
        for (integer i = 0; i < 8; i++) begin
          $dumpvars(0, x[i]);
          $dumpvars(0, h[i]);
        end

        for (integer i = 0; i < 15; i++) begin
          $dumpvars(0, y[i]);
        end

                // Test Case 1
        x[0] = 4'd1; x[1] = 4'd2; x[2] = 4'd3; x[3] = 4'd4;
        x[4] = 4'd5; x[5] = 4'd6; x[6] = 4'd7; x[7] = 4'd8;

        h[0] = 4'd1; h[1] = 4'd1; h[2] = 4'd1; h[3] = 4'd1;
        h[4] = 4'd1; h[5] = 4'd1; h[6] = 4'd1; h[7] = 4'd1;

        #10;

        $display("Test Case 1 Results:");
        for (int i = 0; i < 15; i = i + 1) begin
            $display("y[%0d] = %0d", i, y[i]);
        end

        // Test Case 2
        x[0] = 4'd1; x[1] = 4'd1; x[2] = 4'd1; x[3] = 4'd1;
        x[4] = 4'd1; x[5] = 4'd1; x[6] = 4'd1; x[7] = 4'd1;

        h[0] = 4'd1; h[1] = 4'd1; h[2] = 4'd1; h[3] = 4'd1;
        h[4] = 4'd1; h[5] = 4'd1; h[6] = 4'd1; h[7] = 4'd1;

        #10;

        $display("Test Case 2 Results:");
        for (int i = 0; i < 15; i = i + 1) begin
            $display("y[%0d] = %0d", i, y[i]);
        end

        $finish;
    end
endmodule
