; ModuleID = "stuff"
target triple = "unknown-unknown-unknown"
target datalayout = ""

%"tt" = type {i64, i64, double, [11 x i1], %"tt"*, %".rec_3"}
%".rec_3" = type {i64*, %"tt"*}
%".rec_8" = type {i64, i64, double, i64}
declare i32 @"printf"(i8* %".1", ...)

declare i32 @"scanf"(i8* %".1", ...)

declare i64 @"rand"()

declare i64 @"time"(i1* %".1")

declare void @"srand"(i64 %".1")

declare i8* @"realloc"(i8* %".1", i64 %".2")

@"t" = private constant double 0x3f04f8b588e368f1
@"t4" = private constant double 0x3f04f8b588e368f1
@"t2" = private constant double 0xbf04f8b588e368f1
@"t3" = private constant double 0x3f04f8b588e368f1
@"l" = private constant i64 10
@"l2" = private constant i64 -10
@".len_1" = global i64 11
@".dim_2" = global i64 0
@".len_4" = global i64 3
@".dim_5" = global i64 0
@".len_6" = global i64 2
@".dim_7" = global i64 1
@"def_int" = private global i64 0
@"i" = private global %".rec_8" {i64 0, i64 0, double              0x0, i64 0}
@"itt" = private global %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}
@"arr" = private global [2 x [3 x i64]] [[3 x i64] [i64 0, i64 0, i64 0], [3 x i64] [i64 0, i64 0, i64 0]]
@".len_9" = global i64 7
@".dim_10" = global i64 4
@".len_11" = global i64 6
@".dim_12" = global i64 0
@".len_13" = global i64 2
@".dim_14" = global i64 1
@"arr2" = private global [2 x [6 x [7 x %"tt"]]] [[6 x [7 x %"tt"]] [[7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}]], [6 x [7 x %"tt"]] [[7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}], [7 x %"tt"] [%"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}, %"tt" {i64 0, i64 0, double              0x0, [11 x i1] [i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0, i1 0], %"tt"* null, %".rec_3" {i64* null, %"tt"* null}}]]]
@"bb" = private global i1 0
@"val_ptr_int" = private global i64* null
define i64 @"test"(i64 %".1")
{
entry:
  %"a" = alloca i64
  store i64 %".1", i64* %"a"
  %"test_ret" = alloca i64
  store i64 0, i64* %"test_ret"
  %".5" = getelementptr i64, i64* %"a", i32 0
  %".6" = load i64, i64* %".5"
  %".7" = alloca [4 x i8]
  store [4 x i8] c"%d\0a\00", [4 x i8]* %".7"
  %".9" = alloca i8*
  %".10" = getelementptr [4 x i8], [4 x i8]* %".7", i32 0, i32 0
  store i8* %".10", i8** %".9"
  %".12" = load i8*, i8** %".9"
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i64 %".6")
  %".14" = getelementptr i64, i64* %"test_ret", i32 0
  %".15" = load i64, i64* %".14"
  %".16" = getelementptr i64, i64* %"a", i32 0
  %".17" = load i64, i64* %".16"
  %".18" = mul i64 %".17", 2
  %".19" = call i64 @"test"(i64 %".18")
  store i64 %".19", i64* %".14"
  %".21" = getelementptr i64, i64* %"test_ret", i32 0
  %".22" = load i64, i64* %".21"
  ret i64 %".22"
}

define void @"hi"(i64 %".1")
{
entry:
  %"a" = alloca i64
  store i64 %".1", i64* %"a"
  store i8* getelementptr ([25 x i8], [25 x i8]* @".literal_15", i32 0, i32 0), i8** @".literal_ptr_16"
  %".5" = load i8*, i8** @".literal_ptr_16"
  %".6" = getelementptr i64, i64* %"a", i32 0
  %".7" = load i64, i64* %".6"
  %".8" = alloca [6 x i8]
  store [6 x i8] c"%s%d\0a\00", [6 x i8]* %".8"
  %".10" = alloca i8*
  %".11" = getelementptr [6 x i8], [6 x i8]* %".8", i32 0, i32 0
  store i8* %".11", i8** %".10"
  %".13" = load i8*, i8** %".10"
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13", i8* %".5", i64 %".7")
  ret void
}

@".literal_15" = global [25 x i8] c"Hi, program HelloWorld! \00"
@".literal_ptr_16" = global i8* null
define i32 @"stuff_main"()
{
entry:
  %".2" = getelementptr %".rec_8", %".rec_8"* @"i", i32 0, i32 2
  %".3" = load double, double* %".2"
  store double 0x405bc71c71c6fde7, double* %".2"
  %".5" = load i64, i64* @".dim_7"
  %".6" = sub i64 1, %".5"
  %".7" = load i64, i64* @".dim_5"
  %".8" = sub i64 0, %".7"
  %".9" = getelementptr [2 x [3 x i64]], [2 x [3 x i64]]* @"arr", i32 0, i64 %".6", i64 %".8"
  %".10" = load i64, i64* %".9"
  store i64 25, i64* %".9"
  %".12" = load i64, i64* @".dim_7"
  %".13" = sub i64 2, %".12"
  %".14" = load i64, i64* @".dim_5"
  %".15" = sub i64 0, %".14"
  %".16" = getelementptr [2 x [3 x i64]], [2 x [3 x i64]]* @"arr", i32 0, i64 %".13", i64 %".15"
  %".17" = load i64, i64* %".16"
  %".18" = mul i64 101, -1
  store i64 %".18", i64* %".16"
  %".20" = getelementptr %".rec_8", %".rec_8"* @"i", i32 0, i32 2
  %".21" = load double, double* %".20"
  store double 0x4016000000000000, double* %".20"
  store i8* getelementptr ([15 x i8], [15 x i8]* @".literal_17", i32 0, i32 0), i8** @".literal_ptr_18"
  %".24" = load i8*, i8** @".literal_ptr_18"
  store i8* getelementptr ([2 x i8], [2 x i8]* @".literal_19", i32 0, i32 0), i8** @".literal_ptr_20"
  %".26" = load i8*, i8** @".literal_ptr_20"
  store i8* getelementptr ([4 x i8], [4 x i8]* @".literal_21", i32 0, i32 0), i8** @".literal_ptr_22"
  %".28" = load i8*, i8** @".literal_ptr_22"
  store i8* getelementptr ([3 x i8], [3 x i8]* @".literal_23", i32 0, i32 0), i8** @".literal_ptr_24"
  %".30" = load i8*, i8** @".literal_ptr_24"
  %".31" = load i64, i64* @".dim_7"
  %".32" = sub i64 1, %".31"
  %".33" = load i64, i64* @".dim_5"
  %".34" = sub i64 0, %".33"
  %".35" = getelementptr [2 x [3 x i64]], [2 x [3 x i64]]* @"arr", i32 0, i64 %".32", i64 %".34"
  %".36" = load i64, i64* %".35"
  store i8* getelementptr ([2 x i8], [2 x i8]* @".literal_25", i32 0, i32 0), i8** @".literal_ptr_26"
  %".38" = load i8*, i8** @".literal_ptr_26"
  %".39" = getelementptr %".rec_8", %".rec_8"* @"i", i32 0, i32 0
  %".40" = load i64, i64* %".39"
  %".41" = alloca [20 x i8]
  store [20 x i8] c"%s%d%s%f%s%s%d%s%d\0a\00", [20 x i8]* %".41"
  %".43" = alloca i8*
  %".44" = getelementptr [20 x i8], [20 x i8]* %".41", i32 0, i32 0
  store i8* %".44", i8** %".43"
  %".46" = load i8*, i8** %".43"
  %".47" = call i32 (i8*, ...) @"printf"(i8* %".46", i8* %".24", i64 9, i8* %".26", double 0x3ef4f8b588e368f1, i8* %".28", i8* %".30", i64 %".36", i8* %".38", i64 %".40")
  store i8* getelementptr ([15 x i8], [15 x i8]* @".literal_27", i32 0, i32 0), i8** @".literal_ptr_28"
  %".49" = load i8*, i8** @".literal_ptr_28"
  %".50" = add i64 2, 2
  %".51" = mul i64 %".50", 2
  %".52" = alloca [6 x i8]
  store [6 x i8] c"%s%d\0a\00", [6 x i8]* %".52"
  %".54" = alloca i8*
  %".55" = getelementptr [6 x i8], [6 x i8]* %".52", i32 0, i32 0
  store i8* %".55", i8** %".54"
  %".57" = load i8*, i8** %".54"
  %".58" = call i32 (i8*, ...) @"printf"(i8* %".57", i8* %".49", i64 %".51")
  store i8* getelementptr ([13 x i8], [13 x i8]* @".literal_29", i32 0, i32 0), i8** @".literal_ptr_30"
  %".60" = load i8*, i8** @".literal_ptr_30"
  %".61" = mul i64 2, 2
  %".62" = add i64 %".61", 2
  %".63" = alloca [6 x i8]
  store [6 x i8] c"%s%d\0a\00", [6 x i8]* %".63"
  %".65" = alloca i8*
  %".66" = getelementptr [6 x i8], [6 x i8]* %".63", i32 0, i32 0
  store i8* %".66", i8** %".65"
  %".68" = load i8*, i8** %".65"
  %".69" = call i32 (i8*, ...) @"printf"(i8* %".68", i8* %".60", i64 %".62")
  call void @"hi"(i64 10)
  %".71" = getelementptr %"tt", %"tt"* @"itt", i32 0, i32 4
  %".72" = load %"tt"*, %"tt"** %".71"
  %".73" = getelementptr %"tt", %"tt"* @"itt", i32 0
  store %"tt"* %".73", %"tt"** %".71"
  %".75" = sitofp i64 2 to double
  %".76" = fcmp olt double %".75",              0x0
  br i1 %".76", label %"entry.if", label %"entry.else"
entry.if:
  store i8* getelementptr ([5 x i8], [5 x i8]* @".literal_31", i32 0, i32 0), i8** @".literal_ptr_32"
  %".79" = load i8*, i8** @".literal_ptr_32"
  %".80" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".80"
  %".82" = alloca i8*
  %".83" = getelementptr [4 x i8], [4 x i8]* %".80", i32 0, i32 0
  store i8* %".83", i8** %".82"
  %".85" = load i8*, i8** %".82"
  %".86" = call i32 (i8*, ...) @"printf"(i8* %".85", i8* %".79")
  br label %"entry.endif"
entry.else:
  store i8* getelementptr ([4 x i8], [4 x i8]* @".literal_33", i32 0, i32 0), i8** @".literal_ptr_34"
  %".89" = load i8*, i8** @".literal_ptr_34"
  %".90" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".90"
  %".92" = alloca i8*
  %".93" = getelementptr [4 x i8], [4 x i8]* %".90", i32 0, i32 0
  store i8* %".93", i8** %".92"
  %".95" = load i8*, i8** %".92"
  %".96" = call i32 (i8*, ...) @"printf"(i8* %".95", i8* %".89")
  br label %"entry.endif"
entry.endif:
  %".98" = getelementptr %"tt", %"tt"* @"itt", i32 0, i32 4
  %".99" = load %"tt"*, %"tt"** %".98"
  %".100" = getelementptr %"tt", %"tt"* %".99", i32 0, i32 0
  %".101" = load i64, i64* %".100"
  store i64 10, i64* %".100"
  %".103" = getelementptr %"tt", %"tt"* @"itt", i32 0, i32 4
  %".104" = load %"tt"*, %"tt"** %".103"
  %".105" = getelementptr %"tt", %"tt"* %".104", i32 0, i32 0
  %".106" = load i64, i64* %".105"
  %".107" = alloca [4 x i8]
  store [4 x i8] c"%d\0a\00", [4 x i8]* %".107"
  %".109" = alloca i8*
  %".110" = getelementptr [4 x i8], [4 x i8]* %".107", i32 0, i32 0
  store i8* %".110", i8** %".109"
  %".112" = load i8*, i8** %".109"
  %".113" = call i32 (i8*, ...) @"printf"(i8* %".112", i64 %".106")
  %".114" = getelementptr i64*, i64** @"val_ptr_int", i32 0
  %".115" = load i64*, i64** %".114"
  %".116" = getelementptr %"tt", %"tt"* @"itt", i32 0, i32 4
  %".117" = load %"tt"*, %"tt"** %".116"
  %".118" = getelementptr %"tt", %"tt"* %".117", i32 0, i32 0
  store i64* %".118", i64** %".114"
  %".120" = getelementptr i64*, i64** @"val_ptr_int", i32 0
  %".121" = load i64*, i64** %".120"
  %".122" = getelementptr i64, i64* %".121", i32 0
  %".123" = load i64, i64* %".122"
  store i64 11, i64* %".122"
  %".125" = getelementptr %"tt", %"tt"* @"itt", i32 0, i32 4
  %".126" = load %"tt"*, %"tt"** %".125"
  %".127" = getelementptr %"tt", %"tt"* %".126", i32 0, i32 0
  %".128" = load i64, i64* %".127"
  %".129" = alloca [4 x i8]
  store [4 x i8] c"%d\0a\00", [4 x i8]* %".129"
  %".131" = alloca i8*
  %".132" = getelementptr [4 x i8], [4 x i8]* %".129", i32 0, i32 0
  store i8* %".132", i8** %".131"
  %".134" = load i8*, i8** %".131"
  %".135" = call i32 (i8*, ...) @"printf"(i8* %".134", i64 %".128")
  %".136" = call i64 @"time"(i1* null)
  call void @"srand"(i64 %".136")
  store i8* getelementptr ([13 x i8], [13 x i8]* @".literal_35", i32 0, i32 0), i8** @".literal_ptr_36"
  %".139" = load i8*, i8** @".literal_ptr_36"
  %".140" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".140"
  %".142" = alloca i8*
  %".143" = getelementptr [4 x i8], [4 x i8]* %".140", i32 0, i32 0
  store i8* %".143", i8** %".142"
  %".145" = load i8*, i8** %".142"
  %".146" = call i32 (i8*, ...) @"printf"(i8* %".145", i8* %".139")
  %".147" = call i64 @"rand"()
  %".148" = alloca [4 x i8]
  store [4 x i8] c"%d\0a\00", [4 x i8]* %".148"
  %".150" = alloca i8*
  %".151" = getelementptr [4 x i8], [4 x i8]* %".148", i32 0, i32 0
  store i8* %".151", i8** %".150"
  %".153" = load i8*, i8** %".150"
  %".154" = call i32 (i8*, ...) @"printf"(i8* %".153", i64 %".147")
  %".155" = call i64 @"rand"()
  %".156" = alloca [4 x i8]
  store [4 x i8] c"%d\0a\00", [4 x i8]* %".156"
  %".158" = alloca i8*
  %".159" = getelementptr [4 x i8], [4 x i8]* %".156", i32 0, i32 0
  store i8* %".159", i8** %".158"
  %".161" = load i8*, i8** %".158"
  %".162" = call i32 (i8*, ...) @"printf"(i8* %".161", i64 %".155")
  store i8* getelementptr ([5 x i8], [5 x i8]* @".literal_37", i32 0, i32 0), i8** @".literal_ptr_38"
  %".164" = load i8*, i8** @".literal_ptr_38"
  %".165" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".165"
  %".167" = alloca i8*
  %".168" = getelementptr [4 x i8], [4 x i8]* %".165", i32 0, i32 0
  store i8* %".168", i8** %".167"
  %".170" = load i8*, i8** %".167"
  %".171" = call i32 (i8*, ...) @"printf"(i8* %".170", i8* %".164")
  ret i32 0
}

@".literal_17" = global [15 x i8] c"Hello, World! \00"
@".literal_ptr_18" = global i8* null
@".literal_19" = global [2 x i8] c" \00"
@".literal_ptr_20" = global i8* null
@".literal_21" = global [4 x i8] c" 0 \00"
@".literal_ptr_22" = global i8* null
@".literal_23" = global [3 x i8] c"c \00"
@".literal_ptr_24" = global i8* null
@".literal_25" = global [2 x i8] c" \00"
@".literal_ptr_26" = global i8* null
@".literal_27" = global [15 x i8] c"(2 + 2) * 2 = \00"
@".literal_ptr_28" = global i8* null
@".literal_29" = global [13 x i8] c"2 * 2 + 2 = \00"
@".literal_ptr_30" = global i8* null
@".literal_31" = global [5 x i8] c"yes!\00"
@".literal_ptr_32" = global i8* null
@".literal_33" = global [4 x i8] c"NO!\00"
@".literal_ptr_34" = global i8* null
@".literal_35" = global [13 x i8] c"random test:\00"
@".literal_ptr_36" = global i8* null
@".literal_37" = global [5 x i8] c"bye!\00"
@".literal_ptr_38" = global i8* null