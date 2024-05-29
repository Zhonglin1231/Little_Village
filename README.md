# The Future of human civilization
## Plan
1. 建立简单模型，模拟无外部牵涉的迷你村庄的发展，观察总结规律，验证项目可行性 
2. 阅读历史，社会学著作，学习探索人类社会发展脉络，抽象为模型间交互的参数与公式 
3. 在上述步骤进行顺利的前提下，搜集数据，学习深度学习模型，对复杂数据结构（人，自然属性等）机器学习 
4. 探究人类社会在不同经济科技情况下的终极政治形态与社会形态 
5. 将其可视化出来。就是动态的一个个小点点的移动
   * 启发性视频: https://www.youtube.com/watch?v=TumP6Z7s57M 
6. 使用Pygame实现
   * pygame基础: https://www.youtube.com/watch?v=y9VG3Pztok8
   * 模型实践: https://www.youtube.com/watch?v=gxAaO2rsdIs
     
## Step
1. 建立名为人的类，设置属性（人的特征）与方法（人自身的变化，人与人的交互等）  
   * **属性**
     * 生命值
         * 0-100
     * 幸福感
         * 影响工作效率，有正面或者负面修正，太低会起义
     * 年龄
         * 和死亡率挂钩
     * 性别
     * 职业
         * 村长，民众，劳工...
     * 能力
         * 有些特殊技能：建造，治疗
      * 特殊状态
          * 生病 (扣血，速度变慢...)
      * 学识
        * 可改变工作效率
      * IQ
        * 可增加学习速度
    * **方法**  
      * 
3. 开始随机给参数，跑循环，观察结果，在过程中调整属性与方法
4. 从历史中提取数据，看模型是否能得出相应结果
5. 对未知数据（未来的科技经济人口水平）进行推导
