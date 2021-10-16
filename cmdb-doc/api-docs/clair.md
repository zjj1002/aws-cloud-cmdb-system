[TOC]

# 文档说明
  本接口文档给予《ResfulAPI接口开放规范》编写。

# 功能列表

##  clair docker扫描
### 1. 获取本地docker镜像列表
#### 描述
```
   获取本地docker镜像列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/clair/local_image/ |

#### get 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | key | 模糊查询关键词 |  N  |  String |  18  | 无  | 模糊查询关键词 |
| 2 | page | 当前页码 |  N  |  Int |  2  |  1  | 当前页码    |
|3| size | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | data | 返回数据 | 返回具体数据  |
|  1  | total | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | id | id |  |
|  2  | REPOSITORY | REPOSITORY | 显示 |
|  3  | TAG | tag | 显示 |
|  4  | is_scan | 是否扫描 | 显示 |
|  5  | IMAGE_ID | 镜像id | 显示 |
|  6  | SIZE | 镜像大小 | 显示 |
|  7  | CREATED | 镜像创建时间 | 显示 |
|  8  | last_scan_time | 扫描时间 |               |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8000/v1/cmdb/clair/local_image/"

```

#### 返回数据实例

``` json
{
	"code": 0,
	"msg": "success",
	"total": 43,
	"data": [{
		"id": "2TDsif3n3YU8YM9ypuLWeJ",
		"REPOSITORY": "docker.io/toniblyx/prowler",
		"is_scan": true,
		"TAG": "latest",
		"IMAGE_ID": "a1d9cd4ac075",
		"CREATED": "3 weeks ago",
		"SIZE": "147 MB",
		"last_scan_time": "2020-07-22 03:37:16.420133"
	}, {
		"id": "2XkApEGsPEocccva72aC6t",
		"REPOSITORY": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-frontend",
		"is_scan": false,
		"TAG": "<none>",
		"IMAGE_ID": "26a4bde1421d",
		"CREATED": "13 days ago",
		"SIZE": "128 MB",
		"last_scan_time": "2020-07-22 03:37:16.418639"
	}, {
		"id": "5QY7fknYo8vLECxTxLckUY",
		"REPOSITORY": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-base-js",
		"is_scan": true,
		"TAG": "latest",
		"IMAGE_ID": "a90ba4cbcb5e",
		"CREATED": "3 months ago",
		"SIZE": "197 MB",
		"last_scan_time": "2020-07-22 03:37:16.426303"
	}, {
		"id": "5VXNTWAF3ucgfPZrYjQKiH",
		"REPOSITORY": "quay.io/coreos/clair",
		"is_scan": true,
		"TAG": "v2.0.1",
		"IMAGE_ID": "930044c045e0",
		"CREATED": "3 years ago",
		"SIZE": "387 MB",
		"last_scan_time": "2020-07-22 03:37:16.428796"
	}, {
		"id": "7Q8rtzhZEgAttjmCHgt4iz",
		"REPOSITORY": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-cmdb",
		"is_scan": false,
		"TAG": "<none>",
		"IMAGE_ID": "4f699633935e",
		"CREATED": "5 weeks ago",
		"SIZE": "1.53 GB",
		"last_scan_time": "2020-07-22 03:37:16.423798"
	}, {
		"id": "AbQoLhTCmpq2QrYrQUEwvK",
		"REPOSITORY": "docker.io/arminc/clair-local-scan",
		"is_scan": false,
		"TAG": "latest",
		"IMAGE_ID": "19a6383d0bc5",
		"CREATED": "36 hours ago",
		"SIZE": "459 MB",
		"last_scan_time": "2020-07-22 03:37:16.417424"
	}, {
		"id": "AWQJ7eRcJZAUMYVg535ZXd",
		"REPOSITORY": "docker.io/arminc/clair-local-scan",
		"is_scan": true,
		"TAG": "v2.0.6",
		"IMAGE_ID": "3bd025211032",
		"CREATED": "18 months ago",
		"SIZE": "350 MB",
		"last_scan_time": "2020-07-22 03:37:16.428492"
	}, {
		"id": "bQdq7a8y9juPSotcv93aDD",
		"REPOSITORY": "cmdb-doc_aws-cmdb-gw",
		"is_scan": true,
		"TAG": "latest",
		"IMAGE_ID": "f4113e486b3f",
		"CREATED": "3 weeks ago",
		"SIZE": "281 MB",
		"last_scan_time": "2020-07-22 03:37:16.419827"
	}, {
		"id": "c9pMui6jX5j5PyxZysKCjv",
		"REPOSITORY": "docker.io/objectiflibre/clair-scanner",
		"is_scan": false,
		"TAG": "latest",
		"IMAGE_ID": "5297e58eb4e3",
		"CREATED": "3 weeks ago",
		"SIZE": "16.6 MB",
		"last_scan_time": "2020-07-22 03:37:16.421016"
	}, {
		"id": "CdRvPv4ssVJZWenQdQQ7aD",
		"REPOSITORY": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage",
		"is_scan": false,
		"TAG": "<none>",
		"IMAGE_ID": "e791aa35b7a3",
		"CREATED": "4 weeks ago",
		"SIZE": "798 MB",
		"last_scan_time": "2020-07-22 03:37:16.422955"
	}]
}
```


### 2. 获取本地docker镜像本地扫描结果
#### 描述
```
 获取本地docker镜像列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/cmdb/clair/scan_cliar/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | image | 镜像名称 |  Y  |  String |    | 无  |  |
| 2 | page | 当前页码 |  N  |  Int |    |   1  | 当前页码   |
|3| size | 每页显示数 |  N  |  Int |    |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
| 2  | message | 返回消息 | 消息说明  |
|  3 | data | 返回数据 | 返回具体数据  |
|  4  | total | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | id | vul_id |  |
|  2  | image | image  | 显示 |
|  3  | featurename |     featurename     | 显示 |
|  4  | featureversion | featureversion | 显示 |
|  5  | vulnerability |   vulnerability   | 显示 |
|  6  | namespace | namespace | 显示 |
|  7  | description | description | 显示 |
|  8  | link | link | 显示 |
|  9  | severity | severity | 显示 |
|  10  | fixedby | fixedby | 显示 |
|  11  | scan_time | 扫描时间 | 显示 |


#### 请求URL实例

``` bash
  $ curl -X get http://127.0.0.1:8000/v1/cmdb/clair/scan_cliar/

```

#### 返回数据实例

``` json
{
	"code": 0,
	"msg": "success",
	"total": 131,
	"data": [{
		"last_scan_time": "2020-07-22 03:41:04.512293",
		"id": "vul2Bi47Za9sXaoCxAcsKQ62E",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "glibc",
		"featureversion": "2.28-10",
		"vulnerability": "CVE-2020-1752",
		"namespace": "debian:10",
		"description": "A use-after-free vulnerability introduced in glibc upstream version 2.14 was found in the way the tilde expansion was carried out. Directory paths containing an initial tilde followed by a valid username were affected by this issue. A local attacker could exploit this flaw by creating a specially crafted path that, when processed by the glob function, would potentially lead to arbitrary code execution. This was fixed in version 2.32.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2020-1752",
		"severity": "Low",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.518246",
		"id": "vul2gMk3pJtQMxSLVr5R7jmVY",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "pcre3",
		"featureversion": "2:8.39-12",
		"vulnerability": "CVE-2019-20838",
		"namespace": "debian:10",
		"description": "libpcre in PCRE before 8.43 allows a subject buffer over-read in JIT when UTF is disabled, and \\X or \\R has more than one fixed quantifier, a related issue to CVE-2019-20454.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2019-20838",
		"severity": "Negligible",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.511041",
		"id": "vul2MKUxVvPfwmzPPzufrE6tN",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "sqlite3",
		"featureversion": "3.27.2-3",
		"vulnerability": "CVE-2020-13630",
		"namespace": "debian:10",
		"description": "ext/fts3/fts3.c in SQLite before 3.32.0 has a use-after-free in fts3EvalNextRow, related to the snippet feature.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2020-13630",
		"severity": "Medium",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.512383",
		"id": "vul2sBEQfjorJEJLHtrhYCQxM",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "glibc",
		"featureversion": "2.28-10",
		"vulnerability": "CVE-2020-6096",
		"namespace": "debian:10",
		"description": "An exploitable signed comparison vulnerability exists in the ARMv7 memcpy() implementation of GNU glibc 2.30.9000. Calling memcpy() (on ARMv7 targets that utilize the GNU glibc implementation) with a negative value for the 'num' parameter results in a signed comparison vulnerability. If an attacker underflows the 'num' parameter to memcpy(), this vulnerability could lead to undefined behavior such as writing to out-of-bounds memory and potentially remote code execution. Furthermore, this memcpy() implementation allows for program execution to continue in scenarios where a segmentation fault or crash should have occurred. The dangers occur in that subsequent execution and iterations of this code will be executed with this corrupted data.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2020-6096",
		"severity": "Low",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.514597",
		"id": "vul35p8AVRBPAqa7sQHQC3zHQ",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "libjpeg-turbo",
		"featureversion": "1:1.5.2-2",
		"vulnerability": "CVE-2018-14498",
		"namespace": "debian:10",
		"description": "get_8bit_row in rdbmp.c in libjpeg-turbo through 1.5.90 and MozJPEG through 3.3.1 allows attackers to cause a denial of service (heap-based buffer over-read and application crash) via a crafted 8-bit BMP in which one or more of the color indices is out of range for the number of palette entries.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2018-14498",
		"severity": "Low",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.509598",
		"id": "vul37eGSEWaKevZaeTCebcqHY",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "libgd2",
		"featureversion": "2.2.5-5.2",
		"vulnerability": "CVE-2017-6363",
		"namespace": "debian:10",
		"description": "** DISPUTED ** In the GD Graphics Library (aka LibGD) through 2.2.5, there is a heap-based buffer over-read in tiffWriter in gd_tiff.c. NOTE: the vendor says \"In my opinion this issue should not have a CVE, since the GD and GD2 formats are documented to be 'obsolete, and should only be used for development and testing purposes.'\"",
		"link": "https://security-tracker.debian.org/tracker/CVE-2017-6363",
		"severity": "Medium",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.517210",
		"id": "vul3hmgpoahD65yx5iRPm7QxN",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "patch",
		"featureversion": "2.7.6-3+deb10u1",
		"vulnerability": "CVE-2018-6952",
		"namespace": "debian:10",
		"description": "A double free exists in the another_hunk function in pch.c in GNU patch through 2.7.6.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2018-6952",
		"severity": "Negligible",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.520665",
		"id": "vul3QGQRWK3GBRZFDvheaHBvo",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "apt",
		"featureversion": "1.8.2.1",
		"vulnerability": "CVE-2011-3374",
		"namespace": "debian:10",
		"description": "It was found that apt-key in apt, all versions, do not correctly validate gpg keys with the master keyring, leading to a potential man-in-the-middle attack.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2011-3374",
		"severity": "Negligible",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.512654",
		"id": "vul3rqbv9Nu58UKNYMkyodsSh",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "libgcrypt20",
		"featureversion": "1.8.4-5",
		"vulnerability": "CVE-2019-13627",
		"namespace": "debian:10",
		"description": "It was discovered that there was a ECDSA timing attack in the libgcrypt20 cryptographic library. Version affected: 1.8.4-5, 1.7.6-2+deb9u3, and 1.6.3-2+deb8u4. Versions fixed: 1.8.5-2 and 1.6.3-2+deb8u7.",
		"link": "https://security-tracker.debian.org/tracker/CVE-2019-13627",
		"severity": "Low",
		"fixedby": ""
	}, {
		"last_scan_time": "2020-07-22 03:41:04.516055",
		"id": "vul3U8V3srfWii7BtBTxSRnqX",
		"image": "309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-usage:latest",
		"featurename": "libpng1.6",
		"featureversion": "1.6.36-6",
		"vulnerability": "CVE-2019-6129",
		"namespace": "debian:10",
		"description": "** DISPUTED ** png_create_info_struct in png.c in libpng 1.6.36 has a memory leak, as demonstrated by pngcp. NOTE: a third party has stated \"I don't think it is libpng's job to free this buffer.\"",
		"link": "https://security-tracker.debian.org/tracker/CVE-2019-6129",
		"severity": "Negligible",
		"fixedby": ""
	}]
}
```


