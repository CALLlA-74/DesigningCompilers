; ModuleID = "fibo"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i64 @"rand"()

declare i64 @"time"(i1* %".1")

declare void @"srand"(i64 %".1")

declare i8* @"realloc"(i8* %".1", i64 %".2")

@"n" = private global i64 0
@"m" = private global i64 0
define i64 @"fibo_calc"(i64 %".1")
{
entry:
  %"n" = alloca i64
  store i64 %".1", i64* %"n"
  %"fibo_calc_ret" = alloca i64
  store i64 0, i64* %"fibo_calc_ret"
  %".5" = getelementptr i64, i64* %"n", i32 0
  %".6" = load i64, i64* %".5"
  %".7" = icmp eq i64 %".6", 1
  %".8" = getelementptr i64, i64* %"n", i32 0
  %".9" = load i64, i64* %".8"
  %".10" = icmp eq i64 %".9", 2
  %".11" = or i1 %".7", %".10"
  br i1 %".11", label %"entry.if", label %"entry.else"
entry.if:
  %".13" = getelementptr i64, i64* %"fibo_calc_ret", i32 0
  %".14" = load i64, i64* %".13"
  store i64 1, i64* %".13"
  br label %"entry.endif"
entry.else:
  %".17" = getelementptr i64, i64* %"fibo_calc_ret", i32 0
  %".18" = load i64, i64* %".17"
  %".19" = getelementptr i64, i64* %"n", i32 0
  %".20" = load i64, i64* %".19"
  %".21" = sub i64 %".20", 1
  %".22" = call i64 @"fibo_calc"(i64 %".21")
  %".23" = getelementptr i64, i64* %"n", i32 0
  %".24" = load i64, i64* %".23"
  %".25" = sub i64 %".24", 2
  %".26" = call i64 @"fibo_calc"(i64 %".25")
  %".27" = add i64 %".22", %".26"
  store i64 %".27", i64* %".17"
  br label %"entry.endif"
entry.endif:
  %".30" = getelementptr i64, i64* %"fibo_calc_ret", i32 0
  %".31" = load i64, i64* %".30"
  ret i64 %".31"
}

define i32 @"fibo_main"()
{
entry:
  %".2" = call i64 @"time"(i1* null)
  call void @"srand"(i64 %".2")
  %".4" = getelementptr i64, i64* @"n", i32 0
  %".5" = load i64, i64* %".4"
  %".6" = call i64 @"rand"()
  %".7" = srem i64 %".6", 35
  store i64 %".7", i64* %".4"
  store i8* getelementptr ([6 x i8], [6 x i8]* @".literal_1", i32 0, i32 0), i8** @".literal_ptr_2"
  %".10" = load i8*, i8** @".literal_ptr_2"
  %".11" = getelementptr i64, i64* @"n", i32 0
  %".12" = load i64, i64* %".11"
  store i8* getelementptr ([5 x i8], [5 x i8]* @".literal_3", i32 0, i32 0), i8** @".literal_ptr_4"
  %".14" = load i8*, i8** @".literal_ptr_4"
  %".15" = getelementptr i64, i64* @"n", i32 0
  %".16" = load i64, i64* %".15"
  %".17" = call i64 @"fibo_calc"(i64 %".16")
  %".18" = alloca [10 x i8]
  store [10 x i8] c"%s%d%s%d\0a\00", [10 x i8]* %".18"
  %".20" = alloca i8*
  %".21" = getelementptr [10 x i8], [10 x i8]* %".18", i32 0, i32 0
  store i8* %".21", i8** %".20"
  %".23" = load i8*, i8** %".20"
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", i8* %".10", i64 %".12", i8* %".14", i64 %".17")
  ret i32 0
}

@".literal_1" = global [6 x i8] c"fibo(\00"
@".literal_ptr_2" = global i8* null
@".literal_3" = global [5 x i8] c") = \00"
@".literal_ptr_4" = global i8* null