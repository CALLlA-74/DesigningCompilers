program list_inverse; 

CONST
	min_list_len = 10;
	max_list_len = 25;
	
	min_val = 0;
	max_val = 100;

type node = record
	value: integer;
	next: ^node
end;

ptr_node = ^node;
ptr_ptr_node = ^ptr_node;

var 
	idx: integer;
	head_list: ^node;
	
function gen_val(min_val, max_val: integer): integer;
	begin
		gen_val := (random + min_val) mod max_val;
	end;

function new_node(val: integer): ptr_node;
	var nd: ^node;
	begin
		nd := new(nd);
		nd^.value := val;
		nd^.next := nil;
		new_node := nd;
	end;

function init_list(list_len: integer): ptr_node;
	var curr_node: ^node;
	idx: integer;
	begin
		curr_node := new_node(gen_val(min_val, max_val));
		init_list := curr_node;
		for idx := 2 to list_len do begin
			curr_node^.next := new_node(gen_val(min_val, max_val));
			curr_node := curr_node^.next;
		end;
	end;

procedure inverse_list(head_list: ptr_ptr_node);
	var nxt_node, curr_node, prev_node: ^node;
	begin
		if (head_list <> nil) and (head_list^ <> nil) and (head_list^^.next <> nil) then 
		begin
			nxt_node := head_list^;
			while nxt_node <> nil do begin
				prev_node := curr_node;
				curr_node := nxt_node;
				nxt_node := nxt_node^.next;
				curr_node^.next := prev_node;
			end;
			head_list^ := curr_node;
		end;
	end;

procedure write_list(head: ptr_node);
	begin
		while head <> nil do begin
			write(head^.value, ' ');
			head := head^.next;
		end;
		writeln;
	end;

begin
	randomize;
	head_list := init_list(gen_val(min_list_len, max_list_len));
	
	writeln;
	write('generated list: ');
	write_list(head_list);
	
	inverse_list(@head_list);
	
	write('inversed list: ');
	write_list(head_list);
end.