function [errorCode, MinimumCorrectorPeriod, MaximumCorrectorPeriod, MinimumProfilerPeriod, MaximumProfilerPeriod, MinimumServitudesPeriod, MaximumServitudesPeriod] = ControllerMotionKernelPeriodMinMaxGet(socketId)
%ControllerMotionKernelPeriodMinMaxGet :  Get controller motion kernel min/max periods
%
%	[errorCode, MinimumCorrectorPeriod, MaximumCorrectorPeriod, MinimumProfilerPeriod, MaximumProfilerPeriod, MinimumServitudesPeriod, MaximumServitudesPeriod] = ControllerMotionKernelPeriodMinMaxGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr MinimumCorrectorPeriod
%		doublePtr MaximumCorrectorPeriod
%		doublePtr MinimumProfilerPeriod
%		doublePtr MaximumProfilerPeriod
%		doublePtr MinimumServitudesPeriod
%		doublePtr MaximumServitudesPeriod


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
MinimumCorrectorPeriod = 0;
MaximumCorrectorPeriod = 0;
MinimumProfilerPeriod = 0;
MaximumProfilerPeriod = 0;
MinimumServitudesPeriod = 0;
MaximumServitudesPeriod = 0;

% lib call
[errorCode, MinimumCorrectorPeriod, MaximumCorrectorPeriod, MinimumProfilerPeriod, MaximumProfilerPeriod, MinimumServitudesPeriod, MaximumServitudesPeriod] = calllib('XPS_Q8_drivers', 'ControllerMotionKernelPeriodMinMaxGet', socketId, MinimumCorrectorPeriod, MaximumCorrectorPeriod, MinimumProfilerPeriod, MaximumProfilerPeriod, MinimumServitudesPeriod, MaximumServitudesPeriod);
