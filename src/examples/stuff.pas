program stuff; 
LABEL 1, 2;  
LABEL 3;
CONST t = 4E-5;
	t4 = t;
	t2 = -t;
	t3 = t4;
	l = 10;
	l2 = -l;
TYPE int = integer;
ptr_int = ^integer;
int32 = int;
tt = record 
  a, b: integer;
  c: real;
  t: array[0..l] of boolean;
  next: ^tt;
  ptr: record 
    s: ptr_int;
    next: ^tt
  end
end;
ptr_tt = ^tt;
ptr_ptr_tt = ^ptr_tt;
arr_type = array[1..2, 0..2] of integer;
arr_type2 = arr_type;
VAR
def_int: integer;
i: record 
  a, b: INTEGER;
  c: REAL;
  e: integer
end;
itt: tt;
arr: arr_type;
arr2: array[1..2] of array(.0..5, 4..10.) of tt;
bb: boolean;
val_ptr_int: ptr_int;

function test(a:int): integer;
	begin
		writeln(a);
		test := test(a*2);
	end;

procedure hi(a:int);
	begin
		writeln('Hi, program HelloWorld! ', a);
		{hi(10);}
	end;

begin   
 i.c := 111.111111111;
 {read(i.a, i.b, i.e); }
 arr[1, 0] := 25;
 arr[2][0] := -101;
 i.c := 5.5;
 writeln('Hello, World! ', 9, ' ', 2E-5, ' 0 ', 'c ', arr[1][0], ' ', i.a);
 writeln('(2 + 2) * 2 = ', (2 + 2) * 2);
 writeln('2 * 2 + 2 = ', 2 * 2 + 2);
 {writeln(test(2));}
 hi(10); 
 itt.next := @itt;
 
 if 2 < 0.0 then begin
	writeln('yes!');
 end else begin
	writeln('NO!');
 end;
 itt.next^.a := 10;
 writeln(itt.next^.a);
 val_ptr_int := @itt.next^.a;
 val_ptr_int^ := 11;
 writeln(itt.next^.a);
 randomize;
 writeln('random test:');
 writeln(random);
 writeln(random);
 writeln('bye!');
end.