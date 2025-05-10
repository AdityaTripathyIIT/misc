/*
module convolve(
    input [3:0] x [7:0],
    input [3:0] h [7:0],
    output reg [3:0] out [14:0]
);
  integer i, j, k;
  always @(*) begin
    for (k = 0; k < 15; k = k + 1) out[k] = 0;

    for (i = 0; i < 8; i = i + 1) begin
      for (j = 0; j < 8; j = j + 1) begin 
        out[i + j] = out[i + j] + x[i] * h[j];
      end
    end
  end

endmodule
*/

module convolution(
    input [3:0] x[0:7],  // First input vector (8 elements, 4-bit each)
    input [3:0] h[0:7],  // Second input vector (8 elements, 4-bit each)
    output reg [3:0] y[0:14] // Output vector (15 elements, 4-bit each)
);

    reg [7:0] temp[0:14]; // Temporary array for calculation (8-bit to handle intermediate sums)
    integer i, j;
    
    always @(*) begin
        // Initialize temp array with zeros
        for (i = 0; i < 15; i = i + 1) begin
            temp[i] = 0;
        end
        
        // Perform convolution
        for (i = 0; i < 8; i = i + 1) begin
            for (j = 0; j < 8; j = j + 1) begin
                temp[i+j] = temp[i+j] + (x[i] * h[j]);
            end
        end
        
        // Assign to output (with truncation to 4 bits)
        for (i = 0; i < 15; i = i + 1) begin
            y[i] = temp[i][3:0]; // Take only lower 4 bits
        end
    end
    
endmodule
