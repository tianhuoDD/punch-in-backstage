/*
 Navicat Premium Data Transfer

 Source Server         : romcere
 Source Server Type    : MySQL
 Source Server Version : 80403
 Source Host           : 118.24.140.242:13306
 Source Schema         : punch-in

 Target Server Type    : MySQL
 Target Server Version : 80403
 File Encoding         : 65001

 Date: 17/04/2025 16:11:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for default_svgs
-- ----------------------------
DROP TABLE IF EXISTS `default_svgs`;
CREATE TABLE `default_svgs`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '-- 默认SVG表',
  `svg_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'svg名称',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `svg_name`(`svg_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of default_svgs
-- ----------------------------
INSERT INTO `default_svgs` VALUES (1, 'icon_food', '餐饮');
INSERT INTO `default_svgs` VALUES (2, 'icon_drink', '饮料');
INSERT INTO `default_svgs` VALUES (3, 'icon_snack', '零食');
INSERT INTO `default_svgs` VALUES (4, 'icon_cart', '购物');
INSERT INTO `default_svgs` VALUES (5, 'icon_taobao', '网购');
INSERT INTO `default_svgs` VALUES (6, 'icon_redenvelope', '红包');
INSERT INTO `default_svgs` VALUES (7, 'icon_other', '其他');

-- ----------------------------
-- Table structure for email_codes
-- ----------------------------
DROP TABLE IF EXISTS `email_codes`;
CREATE TABLE `email_codes`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of email_codes
-- ----------------------------
INSERT INTO `email_codes` VALUES (1, '2434260208@qq.com', '737504', '2025-04-17 15:51:10');
INSERT INTO `email_codes` VALUES (2, 'test@qq.com', '958247', '2025-04-17 06:38:02');
INSERT INTO `email_codes` VALUES (3, '231233@qq.com', '807271', '2025-04-17 14:47:37');
INSERT INTO `email_codes` VALUES (4, '2312332@qq.com', '053805', '2025-04-17 15:01:55');
INSERT INTO `email_codes` VALUES (5, '2312332222@qq.com', '251561', '2025-04-17 15:02:03');
INSERT INTO `email_codes` VALUES (6, '2244313284@qq.com', '289673', '2025-04-17 15:02:13');
INSERT INTO `email_codes` VALUES (7, 'wda@qq.com', '463556', '2025-04-17 15:19:12');
INSERT INTO `email_codes` VALUES (8, '2244313285@qq.com', '735142', '2025-04-17 15:19:22');
INSERT INTO `email_codes` VALUES (9, '243426020833@qq.com', '305526', '2025-04-17 15:35:29');

-- ----------------------------
-- Table structure for svgs
-- ----------------------------
DROP TABLE IF EXISTS `svgs`;
CREATE TABLE `svgs`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT 'svg总表',
  `svg_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `svgs_icon_name`(`svg_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 44 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of svgs
-- ----------------------------
INSERT INTO `svgs` VALUES (1, 'icon_bonus', '奖金');
INSERT INTO `svgs` VALUES (2, 'icon_business', '业务');
INSERT INTO `svgs` VALUES (3, 'icon_clothes', '衣服');
INSERT INTO `svgs` VALUES (4, 'icon_daily', '日历');
INSERT INTO `svgs` VALUES (5, 'icon_donate', '捐赠');
INSERT INTO `svgs` VALUES (6, 'icon_entertainment', '娱乐');
INSERT INTO `svgs` VALUES (7, 'icon_bell', '食物');
INSERT INTO `svgs` VALUES (8, 'icon_food', '餐饮');
INSERT INTO `svgs` VALUES (9, 'icon_fuel', '燃料');
INSERT INTO `svgs` VALUES (10, 'icon_houserent', '房子');
INSERT INTO `svgs` VALUES (11, 'icon_intrest', '兴趣');
INSERT INTO `svgs` VALUES (12, 'icon_investment', '投资');
INSERT INTO `svgs` VALUES (13, 'icon_makeup', '化妆品');
INSERT INTO `svgs` VALUES (14, 'icon_medicine', '医疗');
INSERT INTO `svgs` VALUES (15, 'icon_other', '其他');
INSERT INTO `svgs` VALUES (16, 'icon_phone', '手机');
INSERT INTO `svgs` VALUES (17, 'icon_salary', '工资');
INSERT INTO `svgs` VALUES (18, 'icon_shopping', '日常购买');
INSERT INTO `svgs` VALUES (19, 'icon_smoke_wine', '烟酒');
INSERT INTO `svgs` VALUES (20, 'icon_study', '学习');
INSERT INTO `svgs` VALUES (21, 'icon_tour', '旅游');
INSERT INTO `svgs` VALUES (22, 'icon_traffic', '交通');
INSERT INTO `svgs` VALUES (23, 'icon_winning', '奖励');
INSERT INTO `svgs` VALUES (25, 'icon_add', '新增');
INSERT INTO `svgs` VALUES (26, 'icon_cart', '购物');
INSERT INTO `svgs` VALUES (27, 'icon_drink', '饮料');
INSERT INTO `svgs` VALUES (28, 'icon_electricity', '电');
INSERT INTO `svgs` VALUES (29, 'icon_fruit', '水果');
INSERT INTO `svgs` VALUES (30, 'icon_game', '游戏');
INSERT INTO `svgs` VALUES (31, 'icon_gift', '礼物');
INSERT INTO `svgs` VALUES (32, 'icon_love', '爱心');
INSERT INTO `svgs` VALUES (33, 'icon_noodle', '面条');
INSERT INTO `svgs` VALUES (34, 'icon_redenvelope', '红包');
INSERT INTO `svgs` VALUES (35, 'icon_reduce', '减少');
INSERT INTO `svgs` VALUES (36, 'icon_run', '跑步');
INSERT INTO `svgs` VALUES (37, 'icon_star', '收藏');
INSERT INTO `svgs` VALUES (38, 'icon_sweat', '甜品');
INSERT INTO `svgs` VALUES (39, 'icon_taobao', '网购');
INSERT INTO `svgs` VALUES (40, 'icon_transfer', '转账');
INSERT INTO `svgs` VALUES (41, 'icon_treasure', '奢饰品');
INSERT INTO `svgs` VALUES (42, 'icon_water', '水');
INSERT INTO `svgs` VALUES (43, 'icon_snack', '零食');

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `svg` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `income` float NULL DEFAULT NULL,
  `expense` float NULL DEFAULT NULL,
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of transactions
-- ----------------------------
INSERT INTO `transactions` VALUES (1, '2025-03-21', '11', 'icon_bonus', '支付宝', NULL, 36, '备注', 11);
INSERT INTO `transactions` VALUES (2, '2025-03-21', '餐饮', 'icon_food', '支付宝', NULL, 23, '备注', 11);
INSERT INTO `transactions` VALUES (5, '2025-03-25', 'test', 'icon_add', '支付宝', NULL, 26, '备注', 11);
INSERT INTO `transactions` VALUES (6, '2025-03-25', '222', 'icon_winning', '支付宝', NULL, 365, '备注', 11);
INSERT INTO `transactions` VALUES (7, '2025-03-25', '餐饮', 'icon_food', '支付宝', NULL, 36.96, '备注', 11);

-- ----------------------------
-- Table structure for user_details
-- ----------------------------
DROP TABLE IF EXISTS `user_details`;
CREATE TABLE `user_details`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
  `updated_at` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `fk_user_details_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_details
-- ----------------------------
INSERT INTO `user_details` VALUES (2, 11, '我不是管理员2', 'static/uploads/avatars/user_10_2.png', '2025-01-20 08:17:53', '2025-03-21 04:04:29');
INSERT INTO `user_details` VALUES (10, 19, 'test', NULL, '2025-04-17 15:52:07', '2025-04-17 15:52:07');

-- ----------------------------
-- Table structure for user_svgs
-- ----------------------------
DROP TABLE IF EXISTS `user_svgs`;
CREATE TABLE `user_svgs`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '-- 用户的svg配置',
  `user_id` int(0) NOT NULL COMMENT '用户ID',
  `svg_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'svg名称',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_svgs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_svgs
-- ----------------------------
INSERT INTO `user_svgs` VALUES (1, 11, 'icon_food', '餐饮');
INSERT INTO `user_svgs` VALUES (2, 11, 'icon_drink', '饮料');
INSERT INTO `user_svgs` VALUES (3, 11, 'icon_bonus', '11');
INSERT INTO `user_svgs` VALUES (4, 11, 'icon_add', 'test');
INSERT INTO `user_svgs` VALUES (5, 11, 'icon_winning', '222');
INSERT INTO `user_svgs` VALUES (6, 11, 'icon_investment', '222');
INSERT INTO `user_svgs` VALUES (7, 11, 'icon_traffic', '222');
INSERT INTO `user_svgs` VALUES (53, 19, 'icon_food', '餐饮');
INSERT INTO `user_svgs` VALUES (54, 19, 'icon_drink', '饮料');
INSERT INTO `user_svgs` VALUES (55, 19, 'icon_snack', '零食');
INSERT INTO `user_svgs` VALUES (56, 19, 'icon_cart', '购物');
INSERT INTO `user_svgs` VALUES (57, 19, 'icon_taobao', '网购');
INSERT INTO `user_svgs` VALUES (58, 19, 'icon_redenvelope', '红包');
INSERT INTO `user_svgs` VALUES (59, 19, 'icon_other', '其他');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (11, 'admin', '$2b$12$UJRX6ggsl03AOoAJfCvNyOk3DePn4p3X.eaX52EsjDNFsfWBYoSIS', '24342602084@qq.com');
INSERT INTO `users` VALUES (19, 'test', '$2b$12$8nIIaFQwz27iqGaD.RP9T.txmAdzI6tu2KpPQntlyh9sO4xGQxQ9.', '2434260208@qq.com');

SET FOREIGN_KEY_CHECKS = 1;
