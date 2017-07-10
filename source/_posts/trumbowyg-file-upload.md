---
layout: article
title: Trumbowyg 轻量级的 WYSIWYG 编辑器（附带 Laravel 文件上传）
date: 2017-07-10 19:35:32
tags:
- editor
- 文件上传
categories: 个人日志
---


假期写代码，整理一些关于Editor，文件上传相关的东西。

- [editor](#editor)
- [文件上传（Laravel）](#upload)

<h2 id='editor'>Trumbowyg Editor</h2>

Trumbowyg 是一款轻量级的编辑器，可以高度DIY，界面也很简洁。

官方网站：[Trumbowyg](https://alex-d.github.io/Trumbowyg/)

首先下载官方包，在官网可以直接下载。

目录结构如下：

![Pic](/images/2017-7-10-7-47.png)

其中只需要留下 dist 文件夹即可，其余的是文档，例子，直接删除即可。

使用方法很简单，在 view 界面引用相关的 css 文件与 js 文件，这里默认已经引用了Jquery

```html
<link rel="stylesheet" href="/Trumbowyg/dist/ui/trumbowyg.min.css">

<script src="/Trumbowyg/dist/trumbowyg.js"></script>

```
同时需要创建一个 `textarea` 作为 editor 的容器

```
<textarea id="editor" name="editor" rows="10" cols="80"></textarea>
```
接下来就可以使用Trumbowyg 创建一个编辑器出来

```html
<script>
        $('#editor').trumbowyg({
            btnsDef: {
                // 设置上传的3种方法，远程上传，本地上传，图片64位加密
                image: {
                    dropdown: ['insertImage', 'upload'],
                    ico: 'insertImage'
                }
            },
            btns: [
                ['viewHTML'],
                ['formatting'],
                'btnGrp-design',
                ['superscript', 'subscript'],
                'image',
                'btnGrp-justify',
                'btnGrp-lists',
                ['horizontalRule'],
                ['table'],
                ['foreColor', 'backColor'],
                ['removeformat'],
                ['fullscreen']
            ],
            plugins: {
                upload: {
                    serverPath: '/manager/file',
                    fileFieldName: 'upload',
                    usage : 'notice'
                }
            },
            autogrow: true
        });

    </script>
```

其中 `btnsDef` 是自己定义的按钮组，`btns` 是显示出来的按钮，下面是文件上传插件。`autogrow` 参数定义了文本域的自动缩放

显示出来的效果如下：

![Pic](/images/2017-7-10-21-20.png)

![Pic](/images/2017-7-10-21-21.png)

可能你会发现你的下拉图片按钮里面并没有上传图片的选项，因此我们还需要引用一下图片上传的插件。这个文件要在上面的js文件之后引入

```html
<script src="/Trumbowyg/dist/plugins/upload/trumbowyg.upload.js"></script>
```

接下俩介绍 plugins upload 里面的几个参数
- serverPath : 文件上传 Controller 的路径，用于后台处理上传图片
- fileFieldName : 后台接收文件的名字，也就是 `<input name='upload'>`
- usage : 是海痴自己加上的，用于判断上传来源，方便管理，这个不是官方参数，需要自己修改 js 源码

<h2 id='upload'>文件上传（Laravel）</h2>

接下来需要定义后台代码，这里使用Laravel 5.4框架。

配置文件：`config/imageUpload.php`
```php
<?php
/**
 * Created by PhpStorm.
 * User: liebes
 * Date: 2017/7/10
 * Time: 下午3:42
 */

$imageExtensions = [
    'png', 'jpeg', 'jpg', 'bmp'
];

return [
    'max_size' => 1024 * 1024 * 5,  // default 5MB
    'rules' => [
        'notice' => [
            'path' => 'notification',
            'extensions' => $imageExtensions,
            'disk' => 'public',
            'max_size' => 1024 * 1024 * 50
        ],
    ]
];
```
这个配置文件定义了图片上传大小，图片后缀，图片所属等等信息，可以自由定义

Controller 文件 `FileController.class.php`

```php
<?php

namespace App\Http\Controllers\Manager;

use App\Http\Helpers\Resources;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Models\Image;
use Illuminate\Support\Facades\Config;
use Mockery\Exception;

class FileController extends Controller
{
    // 图片上传配置文件
    protected $config;

    // 上传规则
    protected $rules;

    public function __construct()
    {
        $this->config = config('imageUpload');
        $this->rules = array_keys(config('imageUpload.rules'));
    }


    /**
     * 图片上传方法，配置参见config.ImageUpload
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function upload(Request $request){
        $usage = $request->input('usage');
        if(empty($usage) || !$this->checkUsage($usage)){
            return response()->json([
                'message' => '规则不符'
            ]);
        }

        if(!$request->hasFile('upload')){
            return response()->json([
                'message' => '上传失败'
            ]);
        }

        $file = $request->file('upload');
        $size = $file->getSize();
        $extension = $file->extension();

        if(!$this->checkExtension($extension, $usage)){
            return response()->json([
                'message' => '文件类型不符'
            ]);
        }

        if(!$this->checkFileSize($size, $usage)){
            return response()->json([
                'message' => '文件不能大于5M'
            ]);
        }
        $name = $file->hashName();
        $disk = $this->config['rules'][$usage]['disk'];
        $path = $file->store($this->config['rules'][$usage]['path'], $disk);

        $image = Image::createImg([
            'name'  => $name,
            'size'  => $size,
            'extension' => $extension,
            'path'  => $path
        ]);

        return response()->json([
            'success' => true,
            'file' => config('filesystems.disks.'.$disk.'.url').'/'.$path,
            'info' => $image,
        ]);
    }

    /**
     * @param $usage
     * @return bool
     */
    protected function checkUsage($usage){
        return in_array($usage, $this->rules);
    }

    /**
     * @param $extension
     * @param $usage
     * @return bool
     */
    protected function checkExtension($extension, $usage){
        return in_array($extension, $this->config['rules'][$usage]['extensions']);
    }

    /**
     * @param $size
     * @param $usage
     * @return bool
     */
    protected function checkFileSize($size, $usage){
        $max_size = $this->config['rules'][$usage]['max_size'] ?? $this->config['max_size'];
        return $size < $max_size;
    }


}
```
之后在路由里面配置好路由，即可。

```php
Route::post('file', 'FileController@upload');
```

由于这里做了usage的检测，所以需要在上传文件的时候加上usage这个属性，需要修改js文件如下

`trumbowyg.upload.js`

```javascript
plugins: {
    upload: {
        init: function (trumbowyg) {
            trumbowyg.o.plugins.upload = $.extend(true, {}, defaultOptions, trumbowyg.o.plugins.upload || {});
            var btnDef = {
                fn: function () {
                    trumbowyg.saveRange();

                    var file,
                        usage = trumbowyg.o.plugins.upload.usage,
                        prefix = trumbowyg.o.prefix;
                    var $modal = trumbowyg.openModalInsert(
                  ·········
```
在这里加上usage参数

`trumbowyg.upload.js`

```javascript
// Callback
function (values) {
    var data = new FormData();
    data.append(trumbowyg.o.plugins.upload.fileFieldName, file);
    data.append("usage", usage);
    trumbowyg.o.plugins.upload.data.map(function (cur) {
        data.append(cur.name, cur.value);
    });
```
在提交的Form表单里加上usage的参数

修改以上两处即可

当然在提交的时候可能会出现csrftoken miss match 的问题，参考Laravel文档

[Laravel 下的伪造跨站请求保护 CSRF](http://d.laravel-china.org/docs/5.4/csrf#csrf-x-csrf-token)

在html界面头加上 meta 属性
```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

同时在调用ajax方法之前，进行设置
```javascript
<script>
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
</script>
```
以上就是全部的使用Trumbowyg编辑器与laravel文件上传的全部


最后，吐槽一下ckeditor，丫把所有的文件上传界面都定义在一个iframe里，不是异步递交，到死我都没解决出来csrftoken的问题。
