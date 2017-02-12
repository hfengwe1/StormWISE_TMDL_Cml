# -*- coding: utf-8 -*-
"""
Created on Sept. 20, 2016

@author: arthur, fngwei

provide command line input and output for the StormWISE_GrnAcr_cml model
Mainly to show the output by grouping investment with geographical zone, land use,...
User has to input the YAML file name (the result of optimization model)

"""
import yaml
import os
from copy import deepcopy
from StormWISE_GrnAcr_Engine.stormwise_grnacr import stormwise
from StormWISE_GrnAcr_Engine.stormwise_grnacr import evaluate_solution
from StormWISE_GrnAcr_Engine.stormwise_grnacr_benefits_and_bounds import benefit_slopes
from StormWISE_GrnAcr_Engine.stormwise_grnacr_benefits_and_bounds import upper_bounds
from StormWISE_GrnAcr_Engine.stormwise_grnacr_benefits_and_bounds import convert_benefit_units
from StormWISE_GrnAcr_Engine.stormwise_grnacr_benefits_and_bounds import format_and_convert_benefit_dict
from Arts_Python_Tools.tools import multiply_dict_by_constant
from Arts_Python_Tools.tools import format_dict_as_strings

# amplPath = "/Applications/amplide.macosx64/ampl"  # note: you must also set the solver path in stormwise_grnacr.run
amplPath ='C:/AMPL/AMPLide/ampl.exe'
       
def print_output(solutionDict,benefitUnits,benefitConvertUnits):                              
    benTotsByBenefit = solutionDict['benTotsByBenefit']
    displayDict = format_and_convert_benefit_dict(benTotsByBenefit,"%0.2f",benefitConvertUnits,benefitUnits)
    print "Benefits:"
    print yaml.dump(displayDict)

    investmentTotal = solutionDict['investmentTotal']
    investmentTotalMillions = investmentTotal*1e-3  # the unit of cost is $1,000
    print "Total GSI Investment Required to Obtain These Benefits:   $%0.2f Million\n" % investmentTotalMillions
    while True:
        print "\n Choose one of the following options for INVESTMENT details:"
        print "0 - No more details"
        print "1 - By geographic zone"
        print "2 - By land use"
        print "3 - By green infrastructure technology"
        print "4 - By zone and by land use"
        print "5 - By zone and by green infrastructure technology"
        print "6 - By land use and by green infrastructure technology"
        print "7 - By zone and by land use and by green infrastructure technology"
        stringIn = raw_input("Enter your choice: ")
        try:
            displayOption = int(stringIn)
        except ValueError:
            print "\nSORRY:  %s is not an option - TRY AGAIN" % stringIn
            continue
        print ''
        if displayOption == 0:
            break
        elif displayOption == 1:
            showDict = deepcopy(solutionDict['invTotsByZone'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$ %0.2f Million")
            print "Investment Dollars By Zone:"
            print yaml.dump(showDict)
        elif displayOption == 2:
            showDict = deepcopy(solutionDict['invTotsByLanduse'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$ %0.2f Million")
            print "Investment Dollars By Land Use:"
            print yaml.dump(showDict)
        elif displayOption == 3:
            showDict = deepcopy(solutionDict['invTotsByGi'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$ %0.2f Million")
            print "Investment Dollars By GSI Technology:"
            print yaml.dump(showDict)
        elif displayOption == 4:
            showDict = deepcopy(solutionDict['invTotsByZoneByLanduse'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$%0.2f Million")
            print "Investment Dollars By Zone AND By Landuse:"
            print yaml.dump(showDict)
        elif displayOption == 5:
            showDict = deepcopy(solutionDict['invTotsByZoneByGi'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$%0.2f Million")
            print "Investment Dollars By Zone AND By GSI Technology:"
            print yaml.dump(showDict)
        elif displayOption == 6:
            showDict = deepcopy(solutionDict['invTotsByLanduseByGi'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$%0.2f Million")
            print "Investment Dollars By Land Use AND By GSI Technology:"
            print yaml.dump(showDict)
        elif displayOption == 7:
            showDict = deepcopy(solutionDict['decisions'])
            multiply_dict_by_constant(showDict,1e-3)  # convert to $Million
            format_dict_as_strings(showDict,"$%0.4f Million")
            print "Investment Dollars By Zone AND By Land Use AND By GSI Technology:"
            print yaml.dump(showDict)
        else:
            print "SORRY:  %d is not an option - TRY AGAIN" % displayOption
    while True:
        print "\n Choose one of the following options for BENEFIT details:"
        print "0 - No more details"
        print "1 - By geographic zone"
        print "2 - By land use"
        print "3 - By green infrastructure technology"
        print "4 - By zone and by land use"
        print "5 - By zone and by green infrastructure technology"
        print "6 - By land use and by green infrastructure technology"
        print "7 - By zone and by land use and by green infrastructure technology"
        stringIn = raw_input("Enter your choice: ")
        try:
            displayOption = int(stringIn)
        except ValueError:
            print "\nSORRY:  %s is not an option - TRY AGAIN" % stringIn
            continue
        print ''
        if displayOption == 0:
            break
        elif displayOption == 1:
            showDict = deepcopy(solutionDict['benTotsByBenefitByZone'])
            #multiply_dict_by_constant(showDict,1e-6)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.2f",benefitConvertUnits,benefitUnits)
            print "Benefits By Zone:"
            print yaml.dump(displayDict)
        elif displayOption == 2:
            showDict = deepcopy(solutionDict['benTotsByBenefitByLanduse'])
            #multiply_dict_by_constant(showDict,1e-6)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.2f",benefitConvertUnits,benefitUnits)
            print "Benefits By Land Use:"
            print yaml.dump(displayDict)
        elif displayOption == 3:
            showDict = deepcopy(solutionDict['benTotsByBenefitByGi'])
            #multiply_dict_by_constant(showDict,1e-6)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.2f",benefitConvertUnits,benefitUnits)
            print "Benefits By GSI Technology:"
            print yaml.dump(displayDict)
        elif displayOption == 4:
            showDict = deepcopy(solutionDict['benTotsByBenefitByZoneByLanduse'])
            #multiply_dict_by_constant(showDict,1e-6)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.2f",benefitConvertUnits,benefitUnits)
            print "Benefits By Zone AND By Landuse:"
            print yaml.dump(displayDict)
        elif displayOption == 5:
            showDict = deepcopy(solutionDict['benTotsByBenefitByZoneByGi'])
            #multiply_dict_by_constant(showDict,1e-6)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.2f",benefitConvertUnits,benefitUnits)
            print "Benefits By Zone AND By GSI Technology:"
            print yaml.dump(displayDict)
        elif displayOption == 6:
            showDict = deepcopy(solutionDict['benTotsByBenefitByLanduseByGi'])
            #multiply_dict_by_constant(showDict,1e-6)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.2f",benefitConvertUnits,benefitUnits)
            print "Benefits By Land Use AND By GSI Technology:"
            print yaml.dump(displayDict)
        elif displayOption == 7:
            showDict = deepcopy(solutionDict['benefitsByZoneByLanduseByGi'])
            #multiply_dict_by_constant(showDict,1.0)  # convert to $Million
            displayDict = format_and_convert_benefit_dict(showDict,"%0.4f",benefitConvertUnits,benefitUnits)
            print "Benefits By Zone AND By Land Use AND By GSI Technology:"
            print yaml.dump(displayDict)
        else:
            print "SORRY:  %d is not an option - TRY AGAIN" % displayOption


def main():
    print "\n\nStormWISE_GrnAcr COMMAND LINE VERSION\n"
    print "Instructions:"
    print "1. Before running StormWISE, you must prepare an input text file in YAML format"
    print "   and you will specify the name of that file below"
    print "2. StormWISE will calculate and display the MAXIMUM POSSIBLE BENEFITS"
    print "   that can be achieved by installing Green Stormwater Infrastructure (GSI)"
    print "   AT ALL POSSIBLE SITES in the watershed"
    print "3. StormWISE will then display an estimate of the"
    print "   TOTAL WATERSHED-WIDE INVESTMENT DOLLARS required"
    print "   to achieve maximum possible benefits"
    print "4. You will be given several options for showing how the maximum investment dollars"
    print "   and maximum possible benefits would be distributed across geographic zones,"
    print "   land uses, and GSI technologies"
    print "5. Then you will be asked to choose numeric values for"
    print "   the RUNOFF LOAD REDUCTIONS (BENEFIT LEVELS) THAT YOU ACTUALLY WANT TO ACHIEVE,"
    print "   using the units specified"
    print "6. StormWISE will then run its OPTIMIZATION MODEL to"
    print "   find the best way to allocate investment dollars among"
    print "   different geographic zones, land uses, and GSI technologies"
    print "   so as to MINIMIZE TOTAL WATERSHED-WIDE INVESTMENT DOLLARS"
    print "7. The StormWISE solution will be displayed to the screen"
    print "   and you will then be given several options for breaking out optimized benefits"
    print "   and investment dollars according to geographic zone, land use, and GSI technologies"
    print "8. You will then be invited to perform \"Sensitivity Analyses\""
    print "   by entering ALTERNATIVE BENEFIT LEVELS to learn how different runoff load reductions"
    print "   change the total investments required and the distribution of benefits by zones, land uses"
    print "   and GSI technologies"
    # read in the desired benefit unit conversions from convert_benefits.yaml
    with open('convert_benefits_com.yaml', 'r') as fin:
        convertBenefits = yaml.load(fin)
    benefitUnits = convertBenefits['benefitUnits']  # units
    benefitConvertUnits = convertBenefits['benefitConvertUnits']  #benefit values

    prompt ="\nEnter the file name containing your\n  StormWISE input data in YAML format\n  (or type Q to quit) :  "
#    inYamlFile="voah1.yaml"
    while True:
        inYamlFile = raw_input(prompt)
        if inYamlFile == "Q" or inYamlFile == "q":
            print "StormWISE Run Completed"
            break
        try:
            with open(inYamlFile, 'r') as fin:
                inYamlDoc = yaml.load(fin)
                break
        except IOError:
            print "\n SORRY:  the file %s can not be found - TRY AGAIN" % inYamlFile
            
    s = benefit_slopes(inYamlDoc)
    T = inYamlDoc['T']
    Ta = inYamlDoc['Ta']
    upperBounds = upper_bounds(inYamlDoc)
    upperBoundSolutionDict = evaluate_solution(upperBounds,s,inYamlDoc)
    print "\n\n\nUPPER LIMITS ON BENEFITS:\n"
    print_output(upperBoundSolutionDict,benefitUnits,benefitConvertUnits)

    #os.chdir("StormWISE_GrnAcr_Engine")  # change directory to the engine
# Load the benefitDict using console input:
    while True:
        benefitDict = {}
        print "Enter Your Required Minimum Runoff Load Reductions (Benefit Levels) in Specified Units: (Type Q to QUIT)"
        tDict = {}
        bDict = {}
        for t in sorted(T):
            prompt = "%s (%s):  " % (t,benefitUnits[t])
            inString = raw_input(prompt)
            if inString == 'Q'or inString == 'q':
                print "StormWISE Run Completed"
                break
            else:
                tDict[t] = float(inString)/benefitConvertUnits[t]  # convert to fundamental units
        print "\nEnter Your weights for the co-benefits (0~1): (Type Q to QUIT)"
        for t in sorted(Ta):
            prompt = "%s (%s):  " % (t,'weight')
            wString = raw_input(prompt)
            if wString == 'Q'or wString == 'q':
                print "StormWISE Run Completed"
                break
            else:
                bDict[t] = float(wString)  # convert to fundamental units
        break
        benefitDict['benefitLowerBounds'] = tDict
        benefitDict['weights'] = bDict
        print "\n\nRUNNING STORMWISE USING AMPL WITH MINOS SOLVER:\n"
        decisions = stormwise(amplPath,inYamlDoc,benefitDict)
        print "\nDISPLAYING THE StormWISE OPTIMAL SOLUTION:\n"
        solutionDict = evaluate_solution(decisions,s,inYamlDoc)
        print_output(solutionDict,benefitUnits,benefitConvertUnits)

main()
