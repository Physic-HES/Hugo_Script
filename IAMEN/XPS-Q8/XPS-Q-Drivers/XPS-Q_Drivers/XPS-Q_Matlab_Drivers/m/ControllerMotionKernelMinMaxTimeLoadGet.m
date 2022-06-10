function [errorCode, MinimumCPUTotalLoadRatio, MaximumCPUTotalLoadRatio, MinimumCPUCorrectorLoadRatio, MaximumCPUCorrectorLoadRatio, MinimumCPUProfilerLoadRatio, MaximumCPUProfilerLoadRatio, MinimumCPUServitudesLoadRatio, MaximumCPUServitudesLoadRatio] = ControllerMotionKernelMinMaxTimeLoadGet(socketId)
%ControllerMotionKernelMinMaxTimeLoadGet :  Get controller motion kernel minimum and maximum time load
%
%	[errorCode, MinimumCPUTotalLoadRatio, MaximumCPUTotalLoadRatio, MinimumCPUCorrectorLoadRatio, MaximumCPUCorrectorLoadRatio, MinimumCPUProfilerLoadRatio, MaximumCPUProfilerLoadRatio, MinimumCPUServitudesLoadRatio, MaximumCPUServitudesLoadRatio] = ControllerMotionKernelMinMaxTimeLoadGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr MinimumCPUTotalLoadRatio
%		doublePtr MaximumCPUTotalLoadRatio
%		doublePtr MinimumCPUCorrectorLoadRatio
%		doublePtr MaximumCPUCorrectorLoadRatio
%		doublePtr MinimumCPUProfilerLoadRatio
%		doublePtr MaximumCPUProfilerLoadRatio
%		doublePtr MinimumCPUServitudesLoadRatio
%		doublePtr MaximumCPUServitudesLoadRatio


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
MinimumCPUTotalLoadRatio = 0;
MaximumCPUTotalLoadRatio = 0;
MinimumCPUCorrectorLoadRatio = 0;
MaximumCPUCorrectorLoadRatio = 0;
MinimumCPUProfilerLoadRatio = 0;
MaximumCPUProfilerLoadRatio = 0;
MinimumCPUServitudesLoadRatio = 0;
MaximumCPUServitudesLoadRatio = 0;

% lib call
[errorCode, MinimumCPUTotalLoadRatio, MaximumCPUTotalLoadRatio, MinimumCPUCorrectorLoadRatio, MaximumCPUCorrectorLoadRatio, MinimumCPUProfilerLoadRatio, MaximumCPUProfilerLoadRatio, MinimumCPUServitudesLoadRatio, MaximumCPUServitudesLoadRatio] = calllib('XPS_Q8_drivers', 'ControllerMotionKernelMinMaxTimeLoadGet', socketId, MinimumCPUTotalLoadRatio, MaximumCPUTotalLoadRatio, MinimumCPUCorrectorLoadRatio, MaximumCPUCorrectorLoadRatio, MinimumCPUProfilerLoadRatio, MaximumCPUProfilerLoadRatio, MinimumCPUServitudesLoadRatio, MaximumCPUServitudesLoadRatio);
