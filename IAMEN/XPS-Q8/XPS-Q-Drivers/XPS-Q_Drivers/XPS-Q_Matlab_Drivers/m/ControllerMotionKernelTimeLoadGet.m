function [errorCode, CPUTotalLoadRatio, CPUCorrectorLoadRatio, CPUProfilerLoadRatio, CPUServitudesLoadRatio] = ControllerMotionKernelTimeLoadGet(socketId)
%ControllerMotionKernelTimeLoadGet :  Get controller motion kernel time load
%
%	[errorCode, CPUTotalLoadRatio, CPUCorrectorLoadRatio, CPUProfilerLoadRatio, CPUServitudesLoadRatio] = ControllerMotionKernelTimeLoadGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr CPUTotalLoadRatio
%		doublePtr CPUCorrectorLoadRatio
%		doublePtr CPUProfilerLoadRatio
%		doublePtr CPUServitudesLoadRatio


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
CPUTotalLoadRatio = 0;
CPUCorrectorLoadRatio = 0;
CPUProfilerLoadRatio = 0;
CPUServitudesLoadRatio = 0;

% lib call
[errorCode, CPUTotalLoadRatio, CPUCorrectorLoadRatio, CPUProfilerLoadRatio, CPUServitudesLoadRatio] = calllib('XPS_Q8_drivers', 'ControllerMotionKernelTimeLoadGet', socketId, CPUTotalLoadRatio, CPUCorrectorLoadRatio, CPUProfilerLoadRatio, CPUServitudesLoadRatio);
