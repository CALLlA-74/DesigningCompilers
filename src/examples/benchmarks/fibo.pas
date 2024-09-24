program fibo; 

var n, m: integer;

function fibo_calc(n: integer): integer;
	begin
		if (n = 1) or (n = 2) then begin
			fibo_calc := 1;
		end else begin 
			fibo_calc := fibo_calc(n - 1) + fibo_calc(n - 2);
		end;
	end;

begin
	{read(n);}
	randomize;
	n := random mod 35;
	writeln('fibo(', n, ') = ', fibo_calc(n));
end.