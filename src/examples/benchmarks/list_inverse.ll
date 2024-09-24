; ModuleID = "list_inverse"
target triple = "unknown-unknown-unknown"
target datalayout = ""

%"node" = type {i64, %"node"*}
declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i64 @"rand"()

declare i64 @"time"(i1* %".1")

declare void @"srand"(i64 %".1")

declare i8* @"realloc"(i8* %".1", i64 %".2")

@"min_list_len" = private constant i64 10
@"max_list_len" = private constant i64 25
@"min_val" = private constant i64 0
@"max_val" = private constant i64 100
@"idx" = private global i64 0
@"head_list" = private global %"node"* null
define i64 @"gen_val"(i64 %".1", i64 %".2")
{
entry:
  %"min_val" = alloca i64
  store i64 %".1", i64* %"min_val"
  %"max_val" = alloca i64
  store i64 %".2", i64* %"max_val"
  %"gen_val_ret" = alloca i64
  store i64 0, i64* %"gen_val_ret"
  %".7" = getelementptr i64, i64* %"gen_val_ret", i32 0
  %".8" = load i64, i64* %".7"
  %".9" = call i64 @"rand"()
  %".10" = getelementptr i64, i64* %"min_val", i32 0
  %".11" = load i64, i64* %".10"
  %".12" = add i64 %".9", %".11"
  %".13" = getelementptr i64, i64* %"max_val", i32 0
  %".14" = load i64, i64* %".13"
  %".15" = srem i64 %".12", %".14"
  store i64 %".15", i64* %".7"
  %".17" = getelementptr i64, i64* %"gen_val_ret", i32 0
  %".18" = load i64, i64* %".17"
  ret i64 %".18"
}

define %"node"* @"new_node"(i64 %".1")
{
entry:
  %"val" = alloca i64
  store i64 %".1", i64* %"val"
  %"new_node_ret" = alloca %"node"*
  store %"node"* null, %"node"** %"new_node_ret"
  %"nd" = alloca %"node"*
  store %"node"* null, %"node"** %"nd"
  %".6" = getelementptr %"node"*, %"node"** %"nd", i32 0
  %".7" = load %"node"*, %"node"** %".6"
  %".8" = getelementptr %"node"*, %"node"** %"nd", i32 0
  %".9" = load %"node"*, %"node"** %".8"
  %".10" = getelementptr %"node", %"node"* %".9", i64 1
  %".11" = ptrtoint %"node"* %".10" to i64
  %".12" = bitcast %"node"* %".9" to i8*
  %".13" = call i8* @"realloc"(i8* %".12", i64 %".11")
  %".14" = bitcast i8* %".13" to %"node"*
  store %"node"* %".14", %"node"** %".6"
  %".16" = getelementptr %"node"*, %"node"** %"nd", i32 0
  %".17" = load %"node"*, %"node"** %".16"
  %".18" = getelementptr %"node", %"node"* %".17", i32 0, i32 0
  %".19" = load i64, i64* %".18"
  %".20" = getelementptr i64, i64* %"val", i32 0
  %".21" = load i64, i64* %".20"
  store i64 %".21", i64* %".18"
  %".23" = getelementptr %"node"*, %"node"** %"nd", i32 0
  %".24" = load %"node"*, %"node"** %".23"
  %".25" = getelementptr %"node", %"node"* %".24", i32 0, i32 1
  %".26" = load %"node"*, %"node"** %".25"
  %".27" = bitcast i1* null to %"node"*
  store %"node"* %".27", %"node"** %".25"
  %".29" = getelementptr %"node"*, %"node"** %"new_node_ret", i32 0
  %".30" = load %"node"*, %"node"** %".29"
  %".31" = getelementptr %"node"*, %"node"** %"nd", i32 0
  %".32" = load %"node"*, %"node"** %".31"
  store %"node"* %".32", %"node"** %".29"
  %".34" = getelementptr %"node"*, %"node"** %"new_node_ret", i32 0
  %".35" = load %"node"*, %"node"** %".34"
  ret %"node"* %".35"
}

define %"node"* @"init_list"(i64 %".1")
{
entry:
  %"list_len" = alloca i64
  store i64 %".1", i64* %"list_len"
  %"init_list_ret" = alloca %"node"*
  store %"node"* null, %"node"** %"init_list_ret"
  %"curr_node" = alloca %"node"*
  store %"node"* null, %"node"** %"curr_node"
  %"idx" = alloca i64
  store i64 0, i64* %"idx"
  %".7" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".8" = load %"node"*, %"node"** %".7"
  %".9" = getelementptr i64, i64* @"min_val", i32 0
  %".10" = load i64, i64* %".9"
  %".11" = getelementptr i64, i64* @"max_val", i32 0
  %".12" = load i64, i64* %".11"
  %".13" = call i64 @"gen_val"(i64 %".10", i64 %".12")
  %".14" = call %"node"* @"new_node"(i64 %".13")
  store %"node"* %".14", %"node"** %".7"
  %".16" = getelementptr %"node"*, %"node"** %"init_list_ret", i32 0
  %".17" = load %"node"*, %"node"** %".16"
  %".18" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".19" = load %"node"*, %"node"** %".18"
  store %"node"* %".19", %"node"** %".16"
  br label %".prepare_for_1"
.prepare_for_1:
  %".22" = getelementptr i64, i64* %"list_len", i32 0
  %".23" = load i64, i64* %".22"
  store i64 2, i64* %"idx"
  %".25" = icmp sle i64 2, %".23"
  %".26" = icmp sgt i64 1, 0
  %".27" = icmp sge i64 2, %".23"
  %".28" = icmp slt i64 1, 0
  %".29" = and i1 %".25", %".26"
  %".30" = and i1 %".27", %".28"
  %".31" = or i1 %".29", %".30"
  br i1 %".31", label %".cond_2", label %".after_4"
.cond_2:
  %".33" = load i64, i64* %"idx"
  %".34" = icmp sle i64 %".33", %".23"
  br i1 %".34", label %".for_3", label %".after_4"
.for_3:
  %".36" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".37" = load %"node"*, %"node"** %".36"
  %".38" = getelementptr %"node", %"node"* %".37", i32 0, i32 1
  %".39" = load %"node"*, %"node"** %".38"
  %".40" = getelementptr i64, i64* @"min_val", i32 0
  %".41" = load i64, i64* %".40"
  %".42" = getelementptr i64, i64* @"max_val", i32 0
  %".43" = load i64, i64* %".42"
  %".44" = call i64 @"gen_val"(i64 %".41", i64 %".43")
  %".45" = call %"node"* @"new_node"(i64 %".44")
  store %"node"* %".45", %"node"** %".38"
  %".47" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".48" = load %"node"*, %"node"** %".47"
  %".49" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".50" = load %"node"*, %"node"** %".49"
  %".51" = getelementptr %"node", %"node"* %".50", i32 0, i32 1
  %".52" = load %"node"*, %"node"** %".51"
  store %"node"* %".52", %"node"** %".47"
  %".54" = add i64 %".33", 1
  store i64 %".54", i64* %"idx"
  br label %".cond_2"
.after_4:
  %".57" = getelementptr %"node"*, %"node"** %"init_list_ret", i32 0
  %".58" = load %"node"*, %"node"** %".57"
  ret %"node"* %".58"
}

define void @"inverse_list"(%"node"** %".1")
{
entry:
  %"head_list" = alloca %"node"**
  store %"node"** %".1", %"node"*** %"head_list"
  %"nxt_node" = alloca %"node"*
  store %"node"* null, %"node"** %"nxt_node"
  %"curr_node" = alloca %"node"*
  store %"node"* null, %"node"** %"curr_node"
  %"prev_node" = alloca %"node"*
  store %"node"* null, %"node"** %"prev_node"
  %".7" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".8" = load %"node"**, %"node"*** %".7"
  %".9" = icmp ne %"node"** %".8", null
  %".10" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".11" = load %"node"**, %"node"*** %".10"
  %".12" = getelementptr %"node"*, %"node"** %".11", i32 0
  %".13" = load %"node"*, %"node"** %".12"
  %".14" = icmp ne %"node"* %".13", null
  %".15" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".16" = load %"node"**, %"node"*** %".15"
  %".17" = getelementptr %"node"*, %"node"** %".16", i32 0
  %".18" = load %"node"*, %"node"** %".17"
  %".19" = getelementptr %"node", %"node"* %".18", i32 0, i32 1
  %".20" = load %"node"*, %"node"** %".19"
  %".21" = icmp ne %"node"* %".20", null
  %".22" = and i1 %".14", %".21"
  %".23" = and i1 %".9", %".22"
  br i1 %".23", label %"entry.if", label %"entry.endif"
entry.if:
  %".25" = getelementptr %"node"*, %"node"** %"nxt_node", i32 0
  %".26" = load %"node"*, %"node"** %".25"
  %".27" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".28" = load %"node"**, %"node"*** %".27"
  %".29" = getelementptr %"node"*, %"node"** %".28", i32 0
  %".30" = load %"node"*, %"node"** %".29"
  store %"node"* %".30", %"node"** %".25"
  br label %".cond_5"
entry.endif:
  ret void
.cond_5:
  %".33" = getelementptr %"node"*, %"node"** %"nxt_node", i32 0
  %".34" = load %"node"*, %"node"** %".33"
  %".35" = icmp ne %"node"* %".34", null
  br i1 %".35", label %".while_6", label %".after_7"
.while_6:
  %".37" = getelementptr %"node"*, %"node"** %"prev_node", i32 0
  %".38" = load %"node"*, %"node"** %".37"
  %".39" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".40" = load %"node"*, %"node"** %".39"
  store %"node"* %".40", %"node"** %".37"
  %".42" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".43" = load %"node"*, %"node"** %".42"
  %".44" = getelementptr %"node"*, %"node"** %"nxt_node", i32 0
  %".45" = load %"node"*, %"node"** %".44"
  store %"node"* %".45", %"node"** %".42"
  %".47" = getelementptr %"node"*, %"node"** %"nxt_node", i32 0
  %".48" = load %"node"*, %"node"** %".47"
  %".49" = getelementptr %"node"*, %"node"** %"nxt_node", i32 0
  %".50" = load %"node"*, %"node"** %".49"
  %".51" = getelementptr %"node", %"node"* %".50", i32 0, i32 1
  %".52" = load %"node"*, %"node"** %".51"
  store %"node"* %".52", %"node"** %".47"
  %".54" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".55" = load %"node"*, %"node"** %".54"
  %".56" = getelementptr %"node", %"node"* %".55", i32 0, i32 1
  %".57" = load %"node"*, %"node"** %".56"
  %".58" = getelementptr %"node"*, %"node"** %"prev_node", i32 0
  %".59" = load %"node"*, %"node"** %".58"
  store %"node"* %".59", %"node"** %".56"
  br label %".cond_5"
.after_7:
  %".62" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".63" = load %"node"**, %"node"*** %".62"
  %".64" = getelementptr %"node"*, %"node"** %".63", i32 0
  %".65" = load %"node"*, %"node"** %".64"
  %".66" = getelementptr %"node"*, %"node"** %"curr_node", i32 0
  %".67" = load %"node"*, %"node"** %".66"
  store %"node"* %".67", %"node"** %".64"
  br label %"entry.endif"
}

define void @"write_list"(%"node"* %".1")
{
entry:
  %"head" = alloca %"node"*
  store %"node"* %".1", %"node"** %"head"
  br label %".cond_8"
.cond_8:
  %".5" = getelementptr %"node"*, %"node"** %"head", i32 0
  %".6" = load %"node"*, %"node"** %".5"
  %".7" = icmp ne %"node"* %".6", null
  br i1 %".7", label %".while_9", label %".after_10"
.while_9:
  %".9" = getelementptr %"node"*, %"node"** %"head", i32 0
  %".10" = load %"node"*, %"node"** %".9"
  %".11" = getelementptr %"node", %"node"* %".10", i32 0, i32 0
  %".12" = load i64, i64* %".11"
  store i8* getelementptr ([2 x i8], [2 x i8]* @".literal_11", i32 0, i32 0), i8** @".literal_ptr_12"
  %".14" = load i8*, i8** @".literal_ptr_12"
  %".15" = alloca [5 x i8]
  store [5 x i8] c"%d%s\00", [5 x i8]* %".15"
  %".17" = alloca i8*
  %".18" = getelementptr [5 x i8], [5 x i8]* %".15", i32 0, i32 0
  store i8* %".18", i8** %".17"
  %".20" = load i8*, i8** %".17"
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".20", i64 %".12", i8* %".14")
  %".22" = getelementptr %"node"*, %"node"** %"head", i32 0
  %".23" = load %"node"*, %"node"** %".22"
  %".24" = getelementptr %"node"*, %"node"** %"head", i32 0
  %".25" = load %"node"*, %"node"** %".24"
  %".26" = getelementptr %"node", %"node"* %".25", i32 0, i32 1
  %".27" = load %"node"*, %"node"** %".26"
  store %"node"* %".27", %"node"** %".22"
  br label %".cond_8"
.after_10:
  %".30" = alloca [2 x i8]
  store [2 x i8] c"\0a\00", [2 x i8]* %".30"
  %".32" = alloca i8*
  %".33" = getelementptr [2 x i8], [2 x i8]* %".30", i32 0, i32 0
  store i8* %".33", i8** %".32"
  %".35" = load i8*, i8** %".32"
  %".36" = call i32 (i8*, ...) @"printf"(i8* %".35")
  ret void
}

@".literal_11" = global [2 x i8] c" \00"
@".literal_ptr_12" = global i8* null
define i32 @"list_inverse_main"()
{
entry:
  %".2" = call i64 @"time"(i1* null)
  call void @"srand"(i64 %".2")
  %".4" = getelementptr %"node"*, %"node"** @"head_list", i32 0
  %".5" = load %"node"*, %"node"** %".4"
  %".6" = getelementptr i64, i64* @"min_list_len", i32 0
  %".7" = load i64, i64* %".6"
  %".8" = getelementptr i64, i64* @"max_list_len", i32 0
  %".9" = load i64, i64* %".8"
  %".10" = call i64 @"gen_val"(i64 %".7", i64 %".9")
  %".11" = call %"node"* @"init_list"(i64 %".10")
  store %"node"* %".11", %"node"** %".4"
  %".13" = alloca [2 x i8]
  store [2 x i8] c"\0a\00", [2 x i8]* %".13"
  %".15" = alloca i8*
  %".16" = getelementptr [2 x i8], [2 x i8]* %".13", i32 0, i32 0
  store i8* %".16", i8** %".15"
  %".18" = load i8*, i8** %".15"
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18")
  store i8* getelementptr ([17 x i8], [17 x i8]* @".literal_13", i32 0, i32 0), i8** @".literal_ptr_14"
  %".21" = load i8*, i8** @".literal_ptr_14"
  %".22" = alloca [3 x i8]
  store [3 x i8] c"%s\00", [3 x i8]* %".22"
  %".24" = alloca i8*
  %".25" = getelementptr [3 x i8], [3 x i8]* %".22", i32 0, i32 0
  store i8* %".25", i8** %".24"
  %".27" = load i8*, i8** %".24"
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".27", i8* %".21")
  %".29" = getelementptr %"node"*, %"node"** @"head_list", i32 0
  %".30" = load %"node"*, %"node"** %".29"
  call void @"write_list"(%"node"* %".30")
  %".32" = getelementptr %"node"*, %"node"** @"head_list", i32 0
  call void @"inverse_list"(%"node"** %".32")
  store i8* getelementptr ([16 x i8], [16 x i8]* @".literal_15", i32 0, i32 0), i8** @".literal_ptr_16"
  %".35" = load i8*, i8** @".literal_ptr_16"
  %".36" = alloca [3 x i8]
  store [3 x i8] c"%s\00", [3 x i8]* %".36"
  %".38" = alloca i8*
  %".39" = getelementptr [3 x i8], [3 x i8]* %".36", i32 0, i32 0
  store i8* %".39", i8** %".38"
  %".41" = load i8*, i8** %".38"
  %".42" = call i32 (i8*, ...) @"printf"(i8* %".41", i8* %".35")
  %".43" = getelementptr %"node"*, %"node"** @"head_list", i32 0
  %".44" = load %"node"*, %"node"** %".43"
  call void @"write_list"(%"node"* %".44")
  ret i32 0
}

@".literal_13" = global [17 x i8] c"generated list: \00"
@".literal_ptr_14" = global i8* null
@".literal_15" = global [16 x i8] c"inversed list: \00"
@".literal_ptr_16" = global i8* null