function [errorCode, CorrectorOutput] = GroupCorrectorOutputGet(socketId, GroupName, nbElement)
%GroupCorrectorOutputGet :  Return corrector outputs
%
%	[errorCode, CorrectorOutput] = GroupCorrectorOutputGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		doublePtr CorrectorOutput


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CorrectorOutput = [];
for i = 1:nbElement
	CorrectorOutput = [CorrectorOutput 0];
end

% lib call
[errorCode, GroupName, CorrectorOutput] = calllib('XPS_Q8_drivers', 'GroupCorrectorOutputGet', socketId, GroupName, nbElement, CorrectorOutput);
