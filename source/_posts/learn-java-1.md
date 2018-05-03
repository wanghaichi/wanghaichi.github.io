---
layout: article
title: Java SE8 的流库
date: 2018-05-03 16:27:17
tags:
- java
categories: JAVA学习笔记
---

JAVA中，流旨在创建一种关注“做什么而非怎么做”的设计理念，我们无需关心流内具体的实现，而把更多精力放在流需要做什么上面。例如我们需要计算一个字符串数组中，长度大于10的有多少，参见下面的代码清单：

```java
public static void main(String args[]) throws IOException{
    String contents = new String(Files.readAllBytes(Paths.get("/Users/liebes/Desktop/open.route")), StandardCharsets.UTF_8);
    List<String> words = Arrays.asList(contents.split("\\PL+"));
    long count = 0;
    // 怎么做
    for(String s : words){
        if(s.length() > 10) count++;
    }
    System.out.println(count);
    // 做什么
    count = words.stream().filter(s -> s.length() > 10).count();
    System.out.println(count);
    count = words.parallelStream().filter(s -> s.length() > 10).count();
    System.out.println(count);
}
```

第一种方式，是很容易想到的一种，循环遍历计算的一种方法，而第二种则是使用了流的概念。

Stream，流。我们可以理解为水流，所有的流操作都是惰性的，即当你访问数据的时候，相关操作才会执行。我们在水流的行进方向设置我们想要完成的操作，当水流经过时，就会执行相关的操作。例如上面的 `count = words.stream().filter(s -> s.length() > 10).count();` 这一句，filter方法可以理解为一个水阀，控制水流。

## 流的创建方式

---

流的创建方式有很多种，可以使用 Stream 提供的工厂方法，也可以使用集合的转换方法。

当然流可以产生子流，两个流也可以合并成一个流，我们也可以通过某些操作，逐一处理流内的元素，例如 `map flatMap filter` 等方法。

下面是创建流的程序清单

```Java
import java.io.IOException;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    
    // 输出流
    public static <T> void show(String title, Stream<T> stream){
        final int SIZE = 10;
        List<T> firstElements = stream.limit(SIZE + 1).collect(Collectors.toList());
        System.out.println(title + ": ");
        for(int i = 0; i < firstElements.size(); i ++){
            if(i > 0) System.out.print(", ");
            if(i < SIZE)
                System.out.print(firstElements.get(i));
            else
                System.out.println("...");
        }
        System.out.println();
    }

    public static void main(String args[]) throws IOException{
        Path path = Paths.get("/Users/liebes/Desktop/open.route");
        String contents = new String(Files.readAllBytes(path), StandardCharsets.UTF_8);
		
        // 通过 Stream.of ，使用自负转数组获取流
        Stream<String> words = Stream.of(contents.split("\\PL+"));
        show("words", words);

        // 通过 Stream.of ，使用可变长参数
        Stream<String> song = Stream.of("gently", "down", "the", "stream");
        show("song", song);

        // 空流
        Stream<String> silence = Stream.empty();
        show("silence", silence);

        // 使用 lemada
        Stream<String> echos = Stream.generate(() -> "Echo");
        show("echos", echos);
		
        Stream<Double> randoms = Stream.generate(Math::random);
        show("randoms", randoms);

        Stream<BigInteger> integers = Stream.iterate(BigInteger.ONE, n->n.add(BigInteger.ONE));
        show("integers", integers);

        Stream<String> wordsAnotherWay = Pattern.compile("\\PL+").splitAsStream(contents);
        show("wordsAnotherWay", wordsAnotherWay);

        try(Stream<String> lines = Files.lines(path, StandardCharsets.UTF_8)){
            show("lines", lines);
        }
    }
}

```

## 终结操作 & Optional API 使用方式

---

类似 `filter map` 等方法，会生成一个新的子流，也就是一个中间处理，流经过这些方法，数据做了处理，返回仍然是流。这种方法为非终结方法。

类似 `count` 等方法，会返回一个具体的结果，这种操作为非终结操作。

非终结操作可能带来的问题，就是没有满足条件的元素，比如 `findFirst` 方法，如果没有满足条件的元素，则可能导致空指针异常。

Optional 类是一种包装类，他存在的意义在于避免空指针异常的问题（当然这需要正确的使用）。

程序清单如下

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class Main {
    // 返回一个包装 1/x 的Optional类
    public static Optional<Double> inverse(Double x){
        return x == 0 ? Optional.empty() : Optional.of(1 / x);
    }
    
	// 返回一个包装 √x 的Optional类
    public static Optional<Double> squareRoot(Double x){
        return x < 0 ? Optional.empty() : Optional.of(Math.sqrt(x));
    }
	
    public static void main(String args[]) throws IOException{
        Path path = Paths.get("/Users/liebes/Desktop/open.route");
        String contents = new String(Files.readAllBytes(path), StandardCharsets.UTF_8);
        List<String> wordList = Arrays.asList(contents.split("\\PL+"));
		
        Optional<String> optionalValue = wordList.stream()
                .filter(s -> s.contains("index"))
                .findFirst();
        // orElse() 提供包装值不存在的时候的默认值
        System.out.println(optionalValue.orElse("no word") + " contains index");

        Optional<String> optionalString = Optional.empty();
        String result = optionalString.orElse("N/A");
        System.out.println("result: " + result);
        result = optionalString.orElseGet(() -> Locale.getDefault().getDisplayName());
        System.out.println(result);

        try{
            result = optionalString.orElseThrow(IllegalStateException::new);
            System.out.println("result: " + result);
        }catch (Throwable e){
            e.printStackTrace();
        }
        optionalValue = wordList.stream()
                .filter(s -> s.contains("a"))
                .findFirst();
        // ifPresent() 当存在的时候才会执行里面的函数
        optionalValue.ifPresent(s -> System.out.println(s + " contains a"));

        Set<String> results = new HashSet<>();
        optionalValue.ifPresent(results::add);
        Optional<Boolean> added = optionalValue.map(results::add);
        System.out.println(added);

        System.out.println(inverse(4.0).flatMap(Main::squareRoot));
        System.out.println(inverse(-1.0).flatMap(Main::squareRoot));
        System.out.println(inverse(0.0).flatMap(Main::squareRoot));
        Optional<Double> result2 = Optional.of(-4.0)
                .flatMap(Main::inverse).flatMap(Main::squareRoot);
        System.out.println(result2);
    }
}

// output
index contains index
result: N/A
English (United States)
java.lang.IllegalStateException
	at java.util.Optional.orElseThrow(Optional.java:290)
	at Main.main(Main.java:34)
app contains a
Optional[false]
Optional[0.5]
Optional.empty
Optional.empty
Optional.empty
```

## 取出元素

---

取出流中的元素有两种方法，一种是使用 `toArray` 方法，转换成数组，另一种是使用 `iterator` 遍历。

Stream 提供了 collect 方法，通过传入的工厂方法，初始化元素。Collectors 类中提供了许多创建容器的工厂方法。

```Java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    // 将每一个元素中的特定字符过滤掉，返回流
    public static Stream<String> noVowels() throws IOException{
        String contents = new String(Files.readAllBytes(
                Paths.get("/Users/liebes/Desktop/open.route")),
                StandardCharsets.UTF_8
        );
        List<String> wordList = Arrays.asList(contents.split("\\PL+"));
        Stream<String> words = wordList.stream();
        return words.map(s -> s.replaceAll("[aeiouAEIOU]", ""));
    }

    // 显示
    public static <T> void show(String label, Set<T> set){
        System.out.print(label + ": " + set.getClass().getName());
        System.out.println("[" +
                set.stream().limit(10).map(Object::toString)
                        .collect(Collectors.joining(", ")) + "]");
    }

    public static void main(String args[]) throws IOException{
        Iterator<Integer> iter = Stream.iterate(0, n -> n + 1).limit(10).iterator();
        while(iter.hasNext()){
            System.out.println(iter.next());
        }
        // 由于在运行时不能泛化数组，所以返回的类型是 Object[]
        Object[] numbers = Stream.iterate(0, n -> n + 1).limit(10).toArray();
        System.out.println("Object array:" + numbers);

        try{
            Integer number = (Integer) numbers[0];
            System.out.println("number: " + number);
            System.out.println("The following statement throws an exception:");
            Integer[] numbers2 = (Integer[]) numbers;
        }
        catch (ClassCastException e){
            System.out.println(e);
        }

        // 生成特定类型的数组
        Integer[] numbers3 = Stream.iterate(0, n -> n + 1).limit(10).toArray(Integer[]::new);
        System.out.println("Integer array: " + numbers3);

        // 使用 collect 方法
        Set<String> noVowelSet = noVowels().collect(Collectors.toSet());
        show("noVowelSet", noVowelSet);

        TreeSet<String> noVowelTreeSet = noVowels().collect(
                Collectors.toCollection(TreeSet::new)
        );
        show("noVowelTreeSet", noVowelTreeSet);

        String result = noVowels().limit(10).collect(Collectors.joining());
        System.out.println("joining: " + result);
        result = noVowels().limit(10).collect(Collectors.joining(", "));
        System.out.println("joining with commas: " + result);
		
        IntSummaryStatistics summary = noVowels().collect(Collectors.summarizingInt(String::length));
        double averageWordLength = summary.getAverage();
        double maxWordLength = summary.getMax();
        System.out.println("Average word length: " + averageWordLength);
        System.out.println("Max word lengthL: " + maxWordLength);
        System.out.println("forEach: ");
        // forEach 接受一个闭包，类似 map 的用法
        noVowels().limit(10).forEach(System.out::println);
    }
}
```

## 收集结果到映射表

---

有时我们需要把流中的结果收集到映射表中，例如获得一个 id -> name 的一个映射表，此时可以使用 Collectors.toMap() 这个方法。

API 文档如下

> public static <T,K,U,M extends Map<K,U>> Collector<T,?,M> toMap(
> 	Function<? super T,? extends K> keyMapper,
> 	Function<? super T,? extends U> valueMapper, 
> 	BinaryOperator<U> mergeFunction,
> 	Supplier<M> mapSupplier
> )
>
> Returns a `Collector` that accumulates elements into a `Map` whose keys and values are the result of applying the provided mapping functions to the input elements.
>
> If the mapped keys contains duplicates (according to [`Object.equals(Object)`](../../../java/lang/Object.html#equals-java.lang.Object-)), the value mapping function is applied to each equal element, and the results are merged using the provided merging function. The `Map` is created by a provided supplier function.
>
> - Type Parameters:
>
>   `T` - the type of the input elements
>
>   `K` - the output type of the key mapping function
>
>   `U` - the output type of the value mapping function
>
>   `M` - the type of the resulting `Map`
>
> - Parameters:
>
>   `keyMapper` - a mapping function to produce keys
>
>   `valueMapper` - a mapping function to produce values
>
>   `mergeFunction` - a merge function, used to resolve collisions between values associated with the same key, as supplied to [`Map.merge(Object, Object, BiFunction)`](../../../java/util/Map.html#merge-K-V-java.util.function.BiFunction-)
>
>   `mapSupplier` - a function which returns a new, empty `Map` into which the results will be inserted
>
> - Returns:
>
>   a `Collector` which collects elements into a `Map` whose keys are the result of applying a key mapping function to the input elements, and whose values are the result of applying a value mapping function to all input elements equal to the key and combining them using the merge function

其中后两个参数可以缺省。

前两个参数定义了 获取 `Key` 与 `Value` 的函数，当发生冲突的时候，则调用第三个参数进行merge，如果不定义，则点那个 Key 冲突则会抛出异常。

第四个参数定义了返回 `Map` 的具体类型，可以传入任何一个 `Map` 子类的 `Supplier`，例如 `TreeMap::new`。

```java
import java.io.IOException;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static class Person{
        private int id;
        private String name;
        public Person(int id, String name){
            this.id = id;
            this.name = name;
        }

        public int getId(){
            return id;
        }

        public String getName(){
            return name;
        }

        public String toString(){
            return getClass().getName() + "[id=" + id + ", name=" + name;
        }
    }

    public static Stream<Person> people(){
        return Stream.of(new Person(1001, "peter"), new Person(1002, "paul"), new Person(1003, "Mary"));
    }

    public static void main(String args[]) throws IOException {
        // 缺省后两个参数
        Map<Integer, String> idToName = people().collect(
                Collectors.toMap(Person::getId, Person::getName)
        );
        System.out.println("idToName: " + idToName);
		
        // ID -> Person
        Map<Integer, Person> idToPerson = people().collect(
                Collectors.toMap(Person::getId, Function.identity())
        );
        System.out.println("idToPerson: " + idToPerson.getClass().getName() + idToPerson);

        // 当冲突的时候解决办法
        idToPerson = people().collect(
                Collectors.toMap(Person::getId, Function.identity(),
                        (existingValue, newValue) -> { throw new IllegalStateException(); },
                        TreeMap::new)
        );
        System.out.println("idToPerson: " + idToPerson.getClass().getName() + idToPerson);

        Stream<Locale> locales = Stream.of(Locale.getAvailableLocales());
        Map<String, String> languageNames = locales.collect(
                Collectors.toMap(
                        Locale::getDisplayName,
                        Locale::getDisplayLanguage,
                        (existingValue, newValue) -> existingValue
                )
        );
        System.out.println("languageNames: " + languageNames);
        locales = Stream.of(Locale.getAvailableLocales());
        
        // 结果冲突保留所有 Value
        Map<String, Set<String>> countryLanguageSets = locales.collect(
                Collectors.toMap(
                        Locale::getDisplayCountry,
                        l -> Collections.singleton(l.getDisplayLanguage()),
                        (a, b) -> {
                            Set<String> union = new HashSet<>(a);
                            union.addAll(b);
                            return union;
                        }
                )
        );
        System.out.println("countryLanguageSets: " + countryLanguageSets);
    }
}

// output
idToName: {1001=peter, 1002=paul, 1003=Mary}
idToPerson: java.util.HashMap{1001=Main$Person[id=1001, name=peter, 1002=Main$Person[id=1002, name=paul, 1003=Main$Person[id=1003, name=Mary}
idToPerson: java.util.TreeMap{1001=Main$Person[id=1001, name=peter, 1002=Main$Person[id=1002, name=paul, 1003=Main$Person[id=1003, name=Mary}
languageNames: {Japanese (Japan,JP)=Japanese, Ukrainian (Ukraine)=Ukrainian, =, ...
countryLanguageSets: {=[, Italian, Slovak, Russian, Hebrew, Belarusian, Serbian, ...
```

（有一些关于Supplier Function这些接口的使用，百度一下就懂了）

## 聚合操作

---

有时我们需要像数据库操作那样进行数据统计，需要用到一些聚合操作。例如统计每个省份的人数总和。

这里需要详细查看一下 `collect` 方法的API


> **collect**
>
> `<R,A> R collect(Collector<? super T,A,R> collector)`
>
> Performs a [mutable reduction]() operation on the elements of this stream using a `Collector`. A `Collector` encapsulates the functions used as arguments to [`collect(Supplier, BiConsumer, BiConsumer)`](), allowing for reuse of collection strategies and composition of collect operations such as multiple-level grouping or partitioning.
>
> If the stream is parallel, and the `Collector` is [`concurrent`](), and either the stream is unordered or the collector is [`unordered`](), then a concurrent reduction will be performed (see [`Collector`]() for details on concurrent reduction.)
>
> This is a [terminal operation]().
>
> When executed in parallel, multiple intermediate results may be instantiated, populated, and merged so as to maintain isolation of mutable data structures. Therefore, even when executed in parallel with non-thread-safe data structures (such as `ArrayList`), no additional synchronization is needed for a parallel reduction.
>
> **Type Parameters:**
>
> `R` - the type of the result
>
> `A` - the intermediate accumulation type of the `Collector`
>
> **Parameters:**
>
> `collector` - the `Collector` describing the reduction
>
> **Returns:**
>
> the result of the reduction

collect 方法接受一个收集器，返回值由具体收集器来决定。传入收集器的参数为流中元素 T，R为收集器返回的类型。

聚集操作主要使用 groupingBy 方法，该方法接受一个 Function 接口类型的参数，以及一个下游收集器。下游收集器负责处理聚集后子元素的操作。

这里需要明确流的流向，参考下面的代码

聚集操作 -> 每个key对应的子流由mapping收集器收集

-> 将元素类型为 City 的流映射成 String -> 子流由 maxBy 收集器收集

```java
Map<String, Optional<String>> stateToLongestCityName = cities.collect(
        groupingBy(
                City::getState,
                mapping(City::getName, maxBy(Comparator.comparing(String::length)))
        )
);
```

下面是具体的程序清单

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static java.util.stream.Collectors.*;

public class Main {
    public static class City{
        private String name;
        private String state;
        private int population;

        public City(String name, String state, int population) {
            this.name = name;
            this.state = state;
            this.population = population;
        }

        public String getName() {
            return name;
        }

        public String getState() {
            return state;
        }

        public int getPopulation() {
            return population;
        }
    }

    public static Stream<City> readCities(String filename) throws IOException{
        return Files.lines(Paths.get(filename)).map(l -> l.split(", "))
                .map(a -> new City(a[0], a[1], Integer.parseInt(a[2])));
    }

    public static void main(String args[]) throws IOException{
        Stream<Locale> locales = Stream.of(Locale.getAvailableLocales());

        // 使用 toSet 收集器，将结果转换成SET
        locales = Stream.of(Locale.getAvailableLocales());
        Map<String, Set<Locale>> countryToLocaleSet = locales.collect(
                Collectors.groupingBy(Locale::getCountry, toSet())
        );
        System.out.println("countryToLocaleSet: " + countryToLocaleSet);
		
        // 使用 counting 收集器，讲结果转换成计数
        locales = Stream.of(Locale.getAvailableLocales());
        Map<String, Long> countryToLocalesCount = locales.collect(
                Collectors.groupingBy(Locale::getCountry, counting())
        );
        System.out.println("countryToLocalesCount: " + countryToLocalesCount);
		
        // 累加和
        Stream<City> cities = readCities("/Users/liebes/cities.txt");
        Map<String, Integer> stateToCityPopulation = cities.collect(
                Collectors.groupingBy(City::getState, summingInt(City::getPopulation))
        );
        System.out.println("stateToCItyPopulation: " + stateToCityPopulation);

        // 求出最值
        cities = readCities("/Users/liebes/cities.txt");
        Map<String, Optional<String>> stateToLongestCityName = cities.collect(
                groupingBy(
                        City::getState,
                        mapping(City::getName, maxBy(Comparator.comparing(String::length)))
                )
        );
        System.out.println("stateToLongestCityName: " + stateToLongestCityName);
		
        locales = Stream.of(Locale.getAvailableLocales());
        Map<String, Set<String>> countryToLanguages = locales.collect(
                groupingBy(
                        Locale::getDisplayCountry,
                        mapping(Locale::getDisplayLanguage, toSet())
                )
        );
        System.out.println("countryToLanguages: " + countryToLanguages);

        cities = readCities("/Users/liebes/cities.txt");
        Map<String, IntSummaryStatistics> stateToCityPopulationSummary = cities.collect(
                groupingBy(
                        City::getState, summarizingInt(City::getPopulation)
                )
        );
        System.out.println(stateToCityPopulationSummary.get("liaoning"));

        // reducing 操作，第一个参数应该是默认的第一个元素
        cities = readCities("/Users/liebes/cities.txt");
        Map<String, String> stateToCityNames = cities.collect(
                groupingBy(
                        City::getState,
                        reducing("", City::getName, (s, t) -> s.length() == 0 ? t : s + ", " + t)
                )
        );
        System.out.println("stateToCityName1: " + stateToCityNames);
		
        cities = readCities("/Users/liebes/cities.txt");
        stateToCityNames = cities.collect(
                groupingBy(
                        City::getState,
                        mapping(City::getName, joining(", "))
                )
        );
        System.out.println("stateToCityName2: " + stateToCityNames);
     }

}
// output
countryToLocaleSet: {=[, in, sl, ...], DE=[de_DE], PR=[es_PR], HK=[zh_HK], TW=[zh_TW], PT=[pt_PT], HN=[es_HN], DK=[da_DK], LT=[lt_LT], LU=[de_LU, fr_LU], ...}
countryToLocalesCount: {=46, DE=1, PR=1, HK=1, TW=1, HR=1, DO=1, UA=1, YE=1, LY=1, HU=1, QA=1, MA=1, DZ=1, ME=2, ID=1, ...}
stateToCItyPopulation: {jilin=56, tianjin=20, beijing=200, liaoning=259, heilongjiang=70}
stateToLongestCityName: {jilin=Optional[jilin], tianjin=Optional[tianjin], beijing=Optional[beijing], liaoning=Optional[shenyang], heilongjiang=Optional[haerbin]}
countryToLanguages: {=[, Italian, Slovak, Russian, Hebrew, Belarusian, Serbian, German, Slovenian, Swedish, Turkish, Ukrainian, ...], Cyprus=[Greek], Sudan=[Arabic], Malaysia=[Malay], Paraguay=[Spanish], Portugal=[Portuguese], Oman=[Arabic], ...}
IntSummaryStatistics{count=3, sum=259, min=10, average=86.333333, max=149}
stateToCityName1: {jilin=jilin, tianjin=tianjin, beijing=beijing, liaoning=shenyang, yingkou, dalian, heilongjiang=haerbin, mohe}
stateToCityName2: {jilin=jilin, tianjin=tianjin, beijing=beijing, liaoning=shenyang, yingkou, dalian, heilongjiang=haerbin, mohe}
// cities.txt
shenyang, liaoning, 100
tianjin, tianjin, 20
yingkou, liaoning, 10
beijing, beijing, 200
dalian, liaoning, 149
jilin, jilin, 56
haerbin, heilongjiang, 14
mohe, heilongjiang, 56
```

