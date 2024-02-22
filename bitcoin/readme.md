# About Bitcoin Addresses

[reference](https://zhuanlan.zhihu.com/p/631349127)

### private_key
private key, WIF(Wallet Import Format) and WIF-compressed.

### bitcoin_ecdsa
bitcoin public key.  
- 公钥K是椭圆曲线上的一个点，它可以由私钥计算出来，定义的公式为 K = kG.其中k为私钥，G为base point是椭圆曲线secp256k1的一个参数。 如果私钥k="0x1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd",那么通过计算可以得到K的两个坐标为： x="f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a" y="07cf33da18bd734c600b96a72bbc4749d5141c90ec8ac328ae52ddfe2e505bdb"
- 公钥是一个曲线上的坐标，要表达这个坐标，又产生了两种存储方式：
    - Uncompressed 形式：就是把两个坐标（x, y）直接连接在一起，再在前面加个 0x04 前缀即可；
    - Compressed 形式，就是当y为偶数时，编码为02x，当y为奇数时，编码为 03x;
- 基本原理：通过椭圆曲线 $y^2=x^3 + 7$ 和编码的x值，我们可以计算得出y,然后完整拼装的出坐标点原始公钥数据。

### p2pkh
pay to public key hash.

### p2sh
pay to script hash.

### nested_segwit
P2SH_P2WPKH  
在原生的隔离见证地址提出之前，原有的地址基础上，实现隔离见证的方式是在P2SH中嵌入 Pay-to-Witness-Public-Key-Hash（P2WPKH）的方式来实现的。这种形式即为兼容的隔离见证地址，和 P2SH的格式是一样的，节点不升级也能正常使用隔离见证。

### p2wpkh & p2wsh
bc1 开头的地址，是由新的隔离见证脚本生成的地址（P2WPKH 或 P2WSH），是纯正的隔离见证地址。

Bech32 编码由 3 部分组成：
human-readable part，比特币主网固定为 bc；
separator，固定为 1；
data part，由数字和小写字母组成，但排除这 4 个： 1, b, i, o （注：10 个数字加上 26 个小写字母，再减去这 4 个排除的字符，可得 32 个字符）。
有个缺点：如果地址的最后一个字符是 p，则在紧接着 p 之前的位置插入或者删除任意数量的字符 q 都不会使其 checksum 失效。为了缓解 Bech32 的上述缺点，在 BIP0350 中提出了 Bech32m 地址：
对于版本为 0 的原生隔离见证地址，使用以前的 Bech32；
对于版本为 1（或者更高）的原生隔离见证地址，则使用新的 Bech32m。
对于 Bech32m 地址，当版本为 1 时，它们总是以 bc1p 开头（即 Taproot 地址）


