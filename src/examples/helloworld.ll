; ModuleID = "helloworld"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i64 @"rand"()

declare i64 @"time"(i1* %".1")

declare void @"srand"(i64 %".1")

declare i8* @"realloc"(i8* %".1", i64 %".2")

define i32 @"helloworld_main"()
{
entry:
  store i8* getelementptr ([14 x i8], [14 x i8]* @".literal_1", i32 0, i32 0), i8** @".literal_ptr_2"
  %".3" = load i8*, i8** @".literal_ptr_2"
  %".4" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".4"
  %".6" = alloca i8*
  %".7" = getelementptr [4 x i8], [4 x i8]* %".4", i32 0, i32 0
  store i8* %".7", i8** %".6"
  %".9" = load i8*, i8** %".6"
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", i8* %".3")
  ret i32 0
}

@".literal_1" = global [14 x i8] c"Hello, World!\00"
@".literal_ptr_2" = global i8* null