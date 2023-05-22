# point-acquisition

自動入金やポイントサイトからのポイントを取得するプログラム

## Git rules

- コミットメッセージは下記の prefix を使用する。[参考 URL](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type)
  - feat: 新しい機能追加
  - fix: バグ修正
  - docs: ドキュメント修正
  - style: コードスタイル修正
  - refactor: リファクタリング
  - perf: パフォーマンスチューニング
  - test: テストの追加/修正
  - chore: 基盤の修正、ライブラリの追加/削除

## ローカルでの動作確認

```shell
make exec_test TARGET={target}
```

|    サイト       |               target                |
| :-----------:  | :----------------------------------:|
|  オートレース    | deposit_autorace, collect_autorace |
|  SPAT4         | deposit_spat4, collect_spat4       |
|  ポイントインカム | point_income                       |
