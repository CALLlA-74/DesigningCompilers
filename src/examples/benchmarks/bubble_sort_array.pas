program bubble_sort_array; 

CONST
	st = 1;
	array_len = 20;
	
	min_val = 0;
	max_val = 100;

type ptr_int = ^integer;

var 
	arr: array[st..array_len] of integer;
	
function gen_val(min_val, max_val: integer): integer;
	begin
		gen_val := (random + min_val) mod max_val;
	end;

procedure init_array;
	var idx: integer;
	begin
		for idx := st to array_len do begin
			arr[idx] := gen_val(min_val, max_val);
		end;
	end;

procedure swap(a, b: ptr_int);
	begin
		a^ := a^ + b^;
		b^ := a^ - b^;
		a^ := a^ - b^;
	end;

procedure sort_array;
	var i, j: integer;
	begin
		for i := st to array_len do begin
			for j := i to array_len do begin
				if arr[i] > arr[j] then begin
					swap(@arr[i], @arr[j]);
				end;
			end;
		end;
	end;

procedure write_array;
	var idx: integer;
	begin
		for idx := st to array_len do begin
			write(arr[idx], ' ');
		end;
		writeln;
	end;

begin
	randomize;
	init_array;
	
	writeln;
	write('generated array: ');
	write_array;
	
	sort_array;
	
	write('sorted array: ');
	write_array;
end.