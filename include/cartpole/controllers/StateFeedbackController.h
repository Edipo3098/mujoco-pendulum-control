#pragma once
#include <vector>

class StateFeedbackController {

    public:
        StateFeedbackController();
        ~StateFeedbackController();

        void setGains(const std::vector<double>& gains);
        double computeControlInput(const std::vector<double>& state);

};