; ModuleID = "bubble_sort_list"
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

define void @"swap"(%"node"* %".1", %"node"* %".2")
{
entry:
  %"a" = alloca %"node"*
  store %"node"* %".1", %"node"** %"a"
  %"b" = alloca %"node"*
  store %"node"* %".2", %"node"** %"b"
  %".6" = getelementptr %"node"*, %"node"** %"a", i32 0
  %".7" = load %"node"*, %"node"** %".6"
  %".8" = getelementptr %"node", %"node"* %".7", i32 0, i32 0
  %".9" = load i64, i64* %".8"
  %".10" = getelementptr %"node"*, %"node"** %"a", i32 0
  %".11" = load %"node"*, %"node"** %".10"
  %".12" = getelementptr %"node", %"node"* %".11", i32 0, i32 0
  %".13" = load i64, i64* %".12"
  %".14" = getelementptr %"node"*, %"node"** %"b", i32 0
  %".15" = load %"node"*, %"node"** %".14"
  %".16" = getelementptr %"node", %"node"* %".15", i32 0, i32 0
  %".17" = load i64, i64* %".16"
  %".18" = add i64 %".13", %".17"
  store i64 %".18", i64* %".8"
  %".20" = getelementptr %"node"*, %"node"** %"b", i32 0
  %".21" = load %"node"*, %"node"** %".20"
  %".22" = getelementptr %"node", %"node"* %".21", i32 0, i32 0
  %".23" = load i64, i64* %".22"
  %".24" = getelementptr %"node"*, %"node"** %"a", i32 0
  %".25" = load %"node"*, %"node"** %".24"
  %".26" = getelementptr %"node", %"node"* %".25", i32 0, i32 0
  %".27" = load i64, i64* %".26"
  %".28" = getelementptr %"node"*, %"node"** %"b", i32 0
  %".29" = load %"node"*, %"node"** %".28"
  %".30" = getelementptr %"node", %"node"* %".29", i32 0, i32 0
  %".31" = load i64, i64* %".30"
  %".32" = sub i64 %".27", %".31"
  store i64 %".32", i64* %".22"
  %".34" = getelementptr %"node"*, %"node"** %"a", i32 0
  %".35" = load %"node"*, %"node"** %".34"
  %".36" = getelementptr %"node", %"node"* %".35", i32 0, i32 0
  %".37" = load i64, i64* %".36"
  %".38" = getelementptr %"node"*, %"node"** %"a", i32 0
  %".39" = load %"node"*, %"node"** %".38"
  %".40" = getelementptr %"node", %"node"* %".39", i32 0, i32 0
  %".41" = load i64, i64* %".40"
  %".42" = getelementptr %"node"*, %"node"** %"b", i32 0
  %".43" = load %"node"*, %"node"** %".42"
  %".44" = getelementptr %"node", %"node"* %".43", i32 0, i32 0
  %".45" = load i64, i64* %".44"
  %".46" = sub i64 %".41", %".45"
  store i64 %".46", i64* %".36"
  ret void
}

define void @"sort_list"(%"node"** %".1")
{
entry:
  %"head_list" = alloca %"node"**
  store %"node"** %".1", %"node"*** %"head_list"
  %"iter_1" = alloca %"node"*
  store %"node"* null, %"node"** %"iter_1"
  %"iter_2" = alloca %"node"*
  store %"node"* null, %"node"** %"iter_2"
  %".6" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".7" = load %"node"**, %"node"*** %".6"
  %".8" = icmp ne %"node"** %".7", null
  %".9" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".10" = load %"node"**, %"node"*** %".9"
  %".11" = getelementptr %"node"*, %"node"** %".10", i32 0
  %".12" = load %"node"*, %"node"** %".11"
  %".13" = icmp ne %"node"* %".12", null
  %".14" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".15" = load %"node"**, %"node"*** %".14"
  %".16" = getelementptr %"node"*, %"node"** %".15", i32 0
  %".17" = load %"node"*, %"node"** %".16"
  %".18" = getelementptr %"node", %"node"* %".17", i32 0, i32 1
  %".19" = load %"node"*, %"node"** %".18"
  %".20" = icmp ne %"node"* %".19", null
  %".21" = and i1 %".13", %".20"
  %".22" = and i1 %".8", %".21"
  br i1 %".22", label %"entry.if", label %"entry.endif"
entry.if:
  %".24" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".25" = load %"node"*, %"node"** %".24"
  %".26" = getelementptr %"node"**, %"node"*** %"head_list", i32 0
  %".27" = load %"node"**, %"node"*** %".26"
  %".28" = getelementptr %"node"*, %"node"** %".27", i32 0
  %".29" = load %"node"*, %"node"** %".28"
  store %"node"* %".29", %"node"** %".24"
  br label %".cond_5"
entry.endif:
  ret void
.cond_5:
  %".32" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".33" = load %"node"*, %"node"** %".32"
  %".34" = icmp ne %"node"* %".33", null
  br i1 %".34", label %".while_6", label %".after_7"
.while_6:
  %".36" = getelementptr %"node"*, %"node"** %"iter_2", i32 0
  %".37" = load %"node"*, %"node"** %".36"
  %".38" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".39" = load %"node"*, %"node"** %".38"
  %".40" = getelementptr %"node", %"node"* %".39", i32 0, i32 1
  %".41" = load %"node"*, %"node"** %".40"
  store %"node"* %".41", %"node"** %".36"
  br label %".cond_8"
.after_7:
  br label %"entry.endif"
.cond_8:
  %".44" = getelementptr %"node"*, %"node"** %"iter_2", i32 0
  %".45" = load %"node"*, %"node"** %".44"
  %".46" = icmp ne %"node"* %".45", null
  br i1 %".46", label %".while_9", label %".after_10"
.while_9:
  %".48" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".49" = load %"node"*, %"node"** %".48"
  %".50" = getelementptr %"node", %"node"* %".49", i32 0, i32 0
  %".51" = load i64, i64* %".50"
  %".52" = getelementptr %"node"*, %"node"** %"iter_2", i32 0
  %".53" = load %"node"*, %"node"** %".52"
  %".54" = getelementptr %"node", %"node"* %".53", i32 0, i32 0
  %".55" = load i64, i64* %".54"
  %".56" = icmp sgt i64 %".51", %".55"
  br i1 %".56", label %".while_9.if", label %".while_9.endif"
.after_10:
  %".72" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".73" = load %"node"*, %"node"** %".72"
  %".74" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".75" = load %"node"*, %"node"** %".74"
  %".76" = getelementptr %"node", %"node"* %".75", i32 0, i32 1
  %".77" = load %"node"*, %"node"** %".76"
  store %"node"* %".77", %"node"** %".72"
  br label %".cond_5"
.while_9.if:
  %".58" = getelementptr %"node"*, %"node"** %"iter_1", i32 0
  %".59" = load %"node"*, %"node"** %".58"
  %".60" = getelementptr %"node"*, %"node"** %"iter_2", i32 0
  %".61" = load %"node"*, %"node"** %".60"
  call void @"swap"(%"node"* %".59", %"node"* %".61")
  br label %".while_9.endif"
.while_9.endif:
  %".64" = getelementptr %"node"*, %"node"** %"iter_2", i32 0
  %".65" = load %"node"*, %"node"** %".64"
  %".66" = getelementptr %"node"*, %"node"** %"iter_2", i32 0
  %".67" = load %"node"*, %"node"** %".66"
  %".68" = getelementptr %"node", %"node"* %".67", i32 0, i32 1
  %".69" = load %"node"*, %"node"** %".68"
  store %"node"* %".69", %"node"** %".64"
  br label %".cond_8"
}

define void @"write_list"(%"node"* %".1")
{
entry:
  %"head" = alloca %"node"*
  store %"node"* %".1", %"node"** %"head"
  br label %".cond_11"
.cond_11:
  %".5" = getelementptr %"node"*, %"node"** %"head", i32 0
  %".6" = load %"node"*, %"node"** %".5"
  %".7" = icmp ne %"node"* %".6", null
  br i1 %".7", label %".while_12", label %".after_13"
.while_12:
  %".9" = getelementptr %"node"*, %"node"** %"head", i32 0
  %".10" = load %"node"*, %"node"** %".9"
  %".11" = getelementptr %"node", %"node"* %".10", i32 0, i32 0
  %".12" = load i64, i64* %".11"
  store i8* getelementptr ([2 x i8], [2 x i8]* @".literal_14", i32 0, i32 0), i8** @".literal_ptr_15"
  %".14" = load i8*, i8** @".literal_ptr_15"
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
  br label %".cond_11"
.after_13:
  %".30" = alloca [2 x i8]
  store [2 x i8] c"\0a\00", [2 x i8]* %".30"
  %".32" = alloca i8*
  %".33" = getelementptr [2 x i8], [2 x i8]* %".30", i32 0, i32 0
  store i8* %".33", i8** %".32"
  %".35" = load i8*, i8** %".32"
  %".36" = call i32 (i8*, ...) @"printf"(i8* %".35")
  ret void
}

@".literal_14" = global [2 x i8] c" \00"
@".literal_ptr_15" = global i8* null
define i32 @"bubble_sort_list_main"()
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
  store i8* getelementptr ([17 x i8], [17 x i8]* @".literal_16", i32 0, i32 0), i8** @".literal_ptr_17"
  %".21" = load i8*, i8** @".literal_ptr_17"
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
  call void @"sort_list"(%"node"** %".32")
  store i8* getelementptr ([14 x i8], [14 x i8]* @".literal_18", i32 0, i32 0), i8** @".literal_ptr_19"
  %".35" = load i8*, i8** @".literal_ptr_19"
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

@".literal_16" = global [17 x i8] c"generated list: \00"
@".literal_ptr_17" = global i8* null
@".literal_18" = global [14 x i8] c"sorted list: \00"
@".literal_ptr_19" = global i8* null