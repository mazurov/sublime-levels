function Level0() {
    'use strict';
    return function Level1() {
        return function Level2() {
            return function Level3() {
                return function Level4() {
                    var fromLevel4;
                    return function Level5() {
                        return function Level6() {
                            return function Level7() {
                                return function Level8() {
                                    console.warn('Seriously, 10 Levels!?');
                                };
                            };
                        };
                    };
                };
            };
        };
    };
}