; ModuleID = "bubble_sort_array"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i64 @"rand"()

declare i64 @"time"(i1* %".1")

declare void @"srand"(i64 %".1")

declare i8* @"realloc"(i8* %".1", i64 %".2")

@"st" = private constant i64 1
@"array_len" = private constant i64 20
@"min_val" = private constant i64 0
@"max_val" = private constant i64 100
@".len_1" = global i64 20
@".dim_2" = global i64 1
@"arr" = private global [20 x i64] [i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0, i64 0]
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

define void @"init_array"()
{
entry:
  %"idx" = alloca i64
  store i64 0, i64* %"idx"
  br label %".prepare_for_3"
.prepare_for_3:
  %".4" = getelementptr i64, i64* @"st", i32 0
  %".5" = load i64, i64* %".4"
  %".6" = getelementptr i64, i64* @"array_len", i32 0
  %".7" = load i64, i64* %".6"
  store i64 %".5", i64* %"idx"
  %".9" = icmp sle i64 %".5", %".7"
  %".10" = icmp sgt i64 1, 0
  %".11" = icmp sge i64 %".5", %".7"
  %".12" = icmp slt i64 1, 0
  %".13" = and i1 %".9", %".10"
  %".14" = and i1 %".11", %".12"
  %".15" = or i1 %".13", %".14"
  br i1 %".15", label %".cond_4", label %".after_6"
.cond_4:
  %".17" = load i64, i64* %"idx"
  %".18" = icmp sle i64 %".17", %".7"
  br i1 %".18", label %".for_5", label %".after_6"
.for_5:
  %".20" = getelementptr i64, i64* %"idx", i32 0
  %".21" = load i64, i64* %".20"
  %".22" = load i64, i64* @".dim_2"
  %".23" = sub i64 %".21", %".22"
  %".24" = getelementptr [20 x i64], [20 x i64]* @"arr", i32 0, i64 %".23"
  %".25" = load i64, i64* %".24"
  %".26" = getelementptr i64, i64* @"min_val", i32 0
  %".27" = load i64, i64* %".26"
  %".28" = getelementptr i64, i64* @"max_val", i32 0
  %".29" = load i64, i64* %".28"
  %".30" = call i64 @"gen_val"(i64 %".27", i64 %".29")
  store i64 %".30", i64* %".24"
  %".32" = add i64 %".17", 1
  store i64 %".32", i64* %"idx"
  br label %".cond_4"
.after_6:
  ret void
}

define void @"swap"(i64* %".1", i64* %".2")
{
entry:
  %"a" = alloca i64*
  store i64* %".1", i64** %"a"
  %"b" = alloca i64*
  store i64* %".2", i64** %"b"
  %".6" = getelementptr i64*, i64** %"a", i32 0
  %".7" = load i64*, i64** %".6"
  %".8" = getelementptr i64, i64* %".7", i32 0
  %".9" = load i64, i64* %".8"
  %".10" = getelementptr i64*, i64** %"a", i32 0
  %".11" = load i64*, i64** %".10"
  %".12" = getelementptr i64, i64* %".11", i32 0
  %".13" = load i64, i64* %".12"
  %".14" = getelementptr i64*, i64** %"b", i32 0
  %".15" = load i64*, i64** %".14"
  %".16" = getelementptr i64, i64* %".15", i32 0
  %".17" = load i64, i64* %".16"
  %".18" = add i64 %".13", %".17"
  store i64 %".18", i64* %".8"
  %".20" = getelementptr i64*, i64** %"b", i32 0
  %".21" = load i64*, i64** %".20"
  %".22" = getelementptr i64, i64* %".21", i32 0
  %".23" = load i64, i64* %".22"
  %".24" = getelementptr i64*, i64** %"a", i32 0
  %".25" = load i64*, i64** %".24"
  %".26" = getelementptr i64, i64* %".25", i32 0
  %".27" = load i64, i64* %".26"
  %".28" = getelementptr i64*, i64** %"b", i32 0
  %".29" = load i64*, i64** %".28"
  %".30" = getelementptr i64, i64* %".29", i32 0
  %".31" = load i64, i64* %".30"
  %".32" = sub i64 %".27", %".31"
  store i64 %".32", i64* %".22"
  %".34" = getelementptr i64*, i64** %"a", i32 0
  %".35" = load i64*, i64** %".34"
  %".36" = getelementptr i64, i64* %".35", i32 0
  %".37" = load i64, i64* %".36"
  %".38" = getelementptr i64*, i64** %"a", i32 0
  %".39" = load i64*, i64** %".38"
  %".40" = getelementptr i64, i64* %".39", i32 0
  %".41" = load i64, i64* %".40"
  %".42" = getelementptr i64*, i64** %"b", i32 0
  %".43" = load i64*, i64** %".42"
  %".44" = getelementptr i64, i64* %".43", i32 0
  %".45" = load i64, i64* %".44"
  %".46" = sub i64 %".41", %".45"
  store i64 %".46", i64* %".36"
  ret void
}

define void @"sort_array"()
{
entry:
  %"i" = alloca i64
  store i64 0, i64* %"i"
  %"j" = alloca i64
  store i64 0, i64* %"j"
  br label %".prepare_for_7"
.prepare_for_7:
  %".5" = getelementptr i64, i64* @"st", i32 0
  %".6" = load i64, i64* %".5"
  %".7" = getelementptr i64, i64* @"array_len", i32 0
  %".8" = load i64, i64* %".7"
  store i64 %".6", i64* %"i"
  %".10" = icmp sle i64 %".6", %".8"
  %".11" = icmp sgt i64 1, 0
  %".12" = icmp sge i64 %".6", %".8"
  %".13" = icmp slt i64 1, 0
  %".14" = and i1 %".10", %".11"
  %".15" = and i1 %".12", %".13"
  %".16" = or i1 %".14", %".15"
  br i1 %".16", label %".cond_8", label %".after_10"
.cond_8:
  %".18" = load i64, i64* %"i"
  %".19" = icmp sle i64 %".18", %".8"
  br i1 %".19", label %".for_9", label %".after_10"
.for_9:
  br label %".prepare_for_11"
.after_10:
  ret void
.prepare_for_11:
  %".22" = getelementptr i64, i64* %"i", i32 0
  %".23" = load i64, i64* %".22"
  %".24" = getelementptr i64, i64* @"array_len", i32 0
  %".25" = load i64, i64* %".24"
  store i64 %".23", i64* %"j"
  %".27" = icmp sle i64 %".23", %".25"
  %".28" = icmp sgt i64 1, 0
  %".29" = icmp sge i64 %".23", %".25"
  %".30" = icmp slt i64 1, 0
  %".31" = and i1 %".27", %".28"
  %".32" = and i1 %".29", %".30"
  %".33" = or i1 %".31", %".32"
  br i1 %".33", label %".cond_12", label %".after_14"
.cond_12:
  %".35" = load i64, i64* %"j"
  %".36" = icmp sle i64 %".35", %".25"
  br i1 %".36", label %".for_13", label %".after_14"
.for_13:
  %".38" = getelementptr i64, i64* %"i", i32 0
  %".39" = load i64, i64* %".38"
  %".40" = load i64, i64* @".dim_2"
  %".41" = sub i64 %".39", %".40"
  %".42" = getelementptr [20 x i64], [20 x i64]* @"arr", i32 0, i64 %".41"
  %".43" = load i64, i64* %".42"
  %".44" = getelementptr i64, i64* %"j", i32 0
  %".45" = load i64, i64* %".44"
  %".46" = load i64, i64* @".dim_2"
  %".47" = sub i64 %".45", %".46"
  %".48" = getelementptr [20 x i64], [20 x i64]* @"arr", i32 0, i64 %".47"
  %".49" = load i64, i64* %".48"
  %".50" = icmp sgt i64 %".43", %".49"
  br i1 %".50", label %".for_13.if", label %".for_13.endif"
.after_14:
  %".67" = add i64 %".18", 1
  store i64 %".67", i64* %"i"
  br label %".cond_8"
.for_13.if:
  %".52" = getelementptr i64, i64* %"i", i32 0
  %".53" = load i64, i64* %".52"
  %".54" = load i64, i64* @".dim_2"
  %".55" = sub i64 %".53", %".54"
  %".56" = getelementptr [20 x i64], [20 x i64]* @"arr", i32 0, i64 %".55"
  %".57" = getelementptr i64, i64* %"j", i32 0
  %".58" = load i64, i64* %".57"
  %".59" = load i64, i64* @".dim_2"
  %".60" = sub i64 %".58", %".59"
  %".61" = getelementptr [20 x i64], [20 x i64]* @"arr", i32 0, i64 %".60"
  call void @"swap"(i64* %".56", i64* %".61")
  br label %".for_13.endif"
.for_13.endif:
  %".64" = add i64 %".35", 1
  store i64 %".64", i64* %"j"
  br label %".cond_12"
}

define void @"write_array"()
{
entry:
  %"idx" = alloca i64
  store i64 0, i64* %"idx"
  br label %".prepare_for_15"
.prepare_for_15:
  %".4" = getelementptr i64, i64* @"st", i32 0
  %".5" = load i64, i64* %".4"
  %".6" = getelementptr i64, i64* @"array_len", i32 0
  %".7" = load i64, i64* %".6"
  store i64 %".5", i64* %"idx"
  %".9" = icmp sle i64 %".5", %".7"
  %".10" = icmp sgt i64 1, 0
  %".11" = icmp sge i64 %".5", %".7"
  %".12" = icmp slt i64 1, 0
  %".13" = and i1 %".9", %".10"
  %".14" = and i1 %".11", %".12"
  %".15" = or i1 %".13", %".14"
  br i1 %".15", label %".cond_16", label %".after_18"
.cond_16:
  %".17" = load i64, i64* %"idx"
  %".18" = icmp sle i64 %".17", %".7"
  br i1 %".18", label %".for_17", label %".after_18"
.for_17:
  %".20" = getelementptr i64, i64* %"idx", i32 0
  %".21" = load i64, i64* %".20"
  %".22" = load i64, i64* @".dim_2"
  %".23" = sub i64 %".21", %".22"
  %".24" = getelementptr [20 x i64], [20 x i64]* @"arr", i32 0, i64 %".23"
  %".25" = load i64, i64* %".24"
  store i8* getelementptr ([2 x i8], [2 x i8]* @".literal_19", i32 0, i32 0), i8** @".literal_ptr_20"
  %".27" = load i8*, i8** @".literal_ptr_20"
  %".28" = alloca [5 x i8]
  store [5 x i8] c"%d%s\00", [5 x i8]* %".28"
  %".30" = alloca i8*
  %".31" = getelementptr [5 x i8], [5 x i8]* %".28", i32 0, i32 0
  store i8* %".31", i8** %".30"
  %".33" = load i8*, i8** %".30"
  %".34" = call i32 (i8*, ...) @"printf"(i8* %".33", i64 %".25", i8* %".27")
  %".35" = add i64 %".17", 1
  store i64 %".35", i64* %"idx"
  br label %".cond_16"
.after_18:
  %".38" = alloca [2 x i8]
  store [2 x i8] c"\0a\00", [2 x i8]* %".38"
  %".40" = alloca i8*
  %".41" = getelementptr [2 x i8], [2 x i8]* %".38", i32 0, i32 0
  store i8* %".41", i8** %".40"
  %".43" = load i8*, i8** %".40"
  %".44" = call i32 (i8*, ...) @"printf"(i8* %".43")
  ret void
}

@".literal_19" = global [2 x i8] c" \00"
@".literal_ptr_20" = global i8* null
define i32 @"bubble_sort_array_main"()
{
entry:
  %".2" = call i64 @"time"(i1* null)
  call void @"srand"(i64 %".2")
  call void @"init_array"()
  %".5" = alloca [2 x i8]
  store [2 x i8] c"\0a\00", [2 x i8]* %".5"
  %".7" = alloca i8*
  %".8" = getelementptr [2 x i8], [2 x i8]* %".5", i32 0, i32 0
  store i8* %".8", i8** %".7"
  %".10" = load i8*, i8** %".7"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10")
  store i8* getelementptr ([18 x i8], [18 x i8]* @".literal_21", i32 0, i32 0), i8** @".literal_ptr_22"
  %".13" = load i8*, i8** @".literal_ptr_22"
  %".14" = alloca [3 x i8]
  store [3 x i8] c"%s\00", [3 x i8]* %".14"
  %".16" = alloca i8*
  %".17" = getelementptr [3 x i8], [3 x i8]* %".14", i32 0, i32 0
  store i8* %".17", i8** %".16"
  %".19" = load i8*, i8** %".16"
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".19", i8* %".13")
  call void @"write_array"()
  call void @"sort_array"()
  store i8* getelementptr ([15 x i8], [15 x i8]* @".literal_23", i32 0, i32 0), i8** @".literal_ptr_24"
  %".24" = load i8*, i8** @".literal_ptr_24"
  %".25" = alloca [3 x i8]
  store [3 x i8] c"%s\00", [3 x i8]* %".25"
  %".27" = alloca i8*
  %".28" = getelementptr [3 x i8], [3 x i8]* %".25", i32 0, i32 0
  store i8* %".28", i8** %".27"
  %".30" = load i8*, i8** %".27"
  %".31" = call i32 (i8*, ...) @"printf"(i8* %".30", i8* %".24")
  call void @"write_array"()
  ret i32 0
}

@".literal_21" = global [18 x i8] c"generated array: \00"
@".literal_ptr_22" = global i8* null
@".literal_23" = global [15 x i8] c"sorted array: \00"
@".literal_ptr_24" = global i8* null